import graphene  # type: ignore

from typing import Optional

from graphene.types.resolver import dict_resolver  # type: ignore

from .carrier import Carrier
from .customer import Customer
from .pricelist_rate import (
    PricelistRate,
    get_pricelist_rate_by_destination,
    get_least_cost_routing,
)
from ..services import account as account_service
from ..services import storage as storage_service
from .types import BigInt


class AccountType(graphene.Enum):
    PREPAID = "PREPAID"
    POSTPAID = "POSTPAID"


class AccountFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    account_tag = graphene.String()
    customer_tag = graphene.String()
    type = AccountType()
    active = graphene.Boolean()
    with_running_transactions = graphene.Boolean()
    with_long_running_transactions = graphene.Boolean()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "account_tag": self.account_tag,
            "customer_tag": self.customer_tag,
            "type": self.type,
            "active": self.active,
            "with_running_transactions": self.with_running_transactions,
            "with_long_running_transactions": self.with_long_running_transactions,
        }


class AccountTransaction(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    transaction_tag = graphene.String(required=True)
    proxy_tag = graphene.String()
    source = graphene.String()
    source_ip = graphene.String()
    destination = graphene.String()
    carrier_ip = graphene.String()
    tags = graphene.List(graphene.String)
    destination_rate = graphene.Field(PricelistRate)
    in_progress = graphene.Boolean()
    inbound = graphene.Boolean()
    timestamp_begin = graphene.DateTime()
    timestamp_end = graphene.DateTime()


class InputAccountPricelistRate(graphene.InputObjectType):
    pricelist_tag = graphene.String(required=True)
    prefix = graphene.String(required=True)
    datetime_start = graphene.DateTime()
    datetime_end = graphene.DateTime()
    connect_fee = graphene.Int()
    rate = graphene.Int()
    rate_increment = graphene.Int()
    interval_start = graphene.Int()
    carrier_tag = graphene.String()
    description = graphene.String()


class InputAccountTransaction(graphene.InputObjectType):
    transaction_tag = graphene.String(required=True)
    proxy_tag = graphene.String()
    source = graphene.String()
    source_ip = graphene.String()
    destination = graphene.String(required=True)
    carrier_ip = graphene.String()
    tags = graphene.List(graphene.String)
    destination_rate = graphene.Field(InputAccountPricelistRate)
    inbound = graphene.Boolean()
    timestamp_begin = graphene.DateTime(required=True)
    timestamp_end = graphene.DateTime()


class LinkedAccount(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID()
    tenant = graphene.ID(default_value='default')
    account_tag = graphene.String(required=True)
    name = graphene.String()
    type = AccountType(required=True)
    customer_tag = graphene.String()
    customer = graphene.Field(Customer)
    notification_email = graphene.String()
    notification_mobile = graphene.String()
    active = graphene.Boolean(default_value=True)
    balance = BigInt()
    max_concurrent_transactions = graphene.Int()
    running_transactions = graphene.List(AccountTransaction)
    carrier_tags = graphene.List(graphene.String)
    carrier_tags_override = graphene.List(graphene.String)
    pricelist_tags = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    destination_rate = graphene.Field(
        lambda: PricelistRate, destination=graphene.String()
    )

    async def resolve_destination_rate(self, info, destination=None):
        account = Account(**dict(self)) if not isinstance(self, Account) else self
        return await get_pricelist_rate_by_destination(
            info,
            tenant=account.tenant,
            pricelist_tags=account.pricelist_tags,
            carrier_tags=account.carrier_tags,
            carrier_tags_override=account.carrier_tags_override,
            destination=destination,
        )


class Account(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID()
    tenant = graphene.ID(default_value='default')
    account_tag = graphene.String(required=True)
    name = graphene.String()
    type = AccountType(required=True)
    customer_tag = graphene.String()
    customer = graphene.Field(Customer)
    notification_email = graphene.String()
    notification_mobile = graphene.String()
    active = graphene.Boolean(default_value=True)
    balance = BigInt()
    max_concurrent_transactions = graphene.Int()
    running_transactions = graphene.List(AccountTransaction)
    carrier_tags = graphene.List(graphene.String)
    carrier_tags_override = graphene.List(graphene.String)
    pricelist_tags = graphene.List(graphene.String)
    tags = graphene.List(graphene.String)
    linked_accounts = graphene.List(LinkedAccount)
    destination_rate = graphene.Field(
        lambda: PricelistRate, destination=graphene.String(required=True)
    )
    least_cost_routing = graphene.List(
        Carrier, destination=graphene.String(required=True)
    )

    async def resolve_destination_rate(self, info, destination=None):
        account = Account(**dict(self)) if not isinstance(self, Account) else self
        return await get_pricelist_rate_by_destination(
            info,
            tenant=account.tenant,
            pricelist_tags=account.pricelist_tags,
            carrier_tags=account.carrier_tags,
            carrier_tags_override=account.carrier_tags_override,
            destination=destination,
        )

    async def resolve_least_cost_routing(self, info, destination=None):
        account = Account(**dict(self)) if not isinstance(self, Account) else self
        return await get_least_cost_routing(
            info,
            tenant=account.tenant,
            carrier_tags=account.carrier_tags,
            carrier_tags_override=account.carrier_tags_override,
            destination=destination,
        )


class upsertAccount(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        name = graphene.String()
        type = AccountType(required=True)
        customer_tag = graphene.String()
        notification_email = graphene.String()
        notification_mobile = graphene.String()
        active = graphene.Boolean(default_value=True)
        balance = BigInt()
        max_concurrent_transactions = graphene.Int()
        carrier_tags = graphene.List(graphene.String)
        carrier_tags_override = graphene.List(graphene.String)
        pricelist_tags = graphene.List(graphene.String)
        tags = graphene.List(graphene.String)
        linked_accounts = graphene.List(graphene.String)

    class Meta:
        default_resolver = dict_resolver

    Output = Account

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        account_tag: Optional[str] = None,
        name: Optional[str] = None,
        type: Optional[str] = None,
        customer_tag: Optional[str] = None,
        notification_email: Optional[str] = None,
        notification_mobile: Optional[str] = None,
        active: bool = None,
        balance: int = None,
        max_concurrent_transactions: int = None,
        carrier_tags: list = None,
        carrier_tags_override: list = None,
        pricelist_tags: list = None,
        tags: list = None,
        linked_accounts: list = None,
    ):
        if id is None and not (tenant is not None and account_tag is not None):
            raise ValueError("Provide either the id or tenant and account_tag!")
        storage = storage_service.get(info.context["request"])
        return await account_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                account_tag=account_tag,
                name=name,
                type=type,
                customer_tag=customer_tag,
                notification_email=notification_email,
                notification_mobile=notification_mobile,
                active=active,
                balance=balance,
                max_concurrent_transactions=max_concurrent_transactions,
                carrier_tags=carrier_tags,
                carrier_tags_override=carrier_tags_override,
                pricelist_tags=pricelist_tags,
                tags=tags,
                linked_accounts=linked_accounts,
            ),
        )


class deleteAccount(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()

    class Meta:
        default_resolver = dict_resolver

    Output = Account

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        account_tag: Optional[str] = None,
    ):
        if id is None and not (tenant is not None and account_tag is not None):
            raise ValueError("Provide either the id or tenant and account_tag!")
        storage = storage_service.get(info.context["request"])
        return await account_service.delete(
            storage, id=id, tenant=tenant, account_tag=account_tag
        )


class incrementAccountBalance(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        tags = graphene.List(graphene.String)
        balance = BigInt()

    ok = graphene.Boolean()

    async def mutate(
        self, info, tenant=None, account_tag=None, tags=None, balance=None
    ):
        storage = storage_service.get(info.context["request"])
        ok = await account_service.increment_balance(
            storage, tenant, account_tag, tags, balance
        )
        return incrementAccountBalance(ok=ok)


class setAccountBalance(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        tags = graphene.List(graphene.String)
        balance = BigInt()

    ok = graphene.Boolean()

    async def mutate(
        self, info, tenant=None, account_tag=None, tags=None, balance=None
    ):
        storage = storage_service.get(info.context["request"])
        ok = await account_service.set_balance(
            storage, tenant, account_tag, tags, balance
        )
        return incrementAccountBalance(ok=ok)


class beginAccountTransaction(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        transaction = graphene.Argument(InputAccountTransaction)

    ok = graphene.Boolean()
    transaction = graphene.Field(AccountTransaction)

    async def mutate(self, info, tenant=None, account_tag=None, transaction=None):
        storage = storage_service.get(info.context["request"])
        transaction = await account_service.begin_transaction(
            storage,
            tenant,
            account_tag,
            {
                "destination_rate": transaction.destination_rate,
                "transaction_tag": transaction.transaction_tag,
                "proxy_tag": transaction.proxy_tag,
                "source": transaction.source,
                "source_ip": transaction.source_ip,
                "destination": transaction.destination,
                "carrier_ip": transaction.carrier_ip,
                "inbound": transaction.inbound,
                "tags": transaction.tags,
                "timestamp_begin": transaction.timestamp_begin,
            },
        )
        return beginAccountTransaction(
            ok=bool(transaction) if transaction is not None else None,
            transaction=transaction,
        )


class endAccountTransaction(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        transaction_tag = graphene.String()
        timestamp_end = graphene.DateTime()

    ok = graphene.Boolean()
    transaction = graphene.Field(AccountTransaction)

    async def mutate(
        self,
        info,
        tenant=None,
        account_tag=None,
        transaction_tag=None,
        timestamp_end=None,
    ):
        storage = storage_service.get(info.context["request"])
        transaction = await account_service.end_transaction(
            storage, tenant, account_tag, transaction_tag, timestamp_end
        )
        return endAccountTransaction(
            ok=bool(transaction) if transaction is not None else None,
            transaction=transaction,
        )


class commitAccountTransaction(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        transaction_tag = graphene.String()
        fee = graphene.Int()

    ok = graphene.Boolean()

    async def mutate(
        self, info, tenant=None, account_tag=None, transaction_tag=None, fee=None
    ):
        storage = storage_service.get(info.context["request"])
        ok = await account_service.commit_transaction(
            storage, tenant, account_tag, transaction_tag, fee
        )
        return commitAccountTransaction(ok=ok)


class rollbackAccountTransaction(graphene.Mutation):
    class Arguments:
        tenant = graphene.ID(default_value='default')
        account_tag = graphene.String()
        transaction_tag = graphene.String()

    ok = graphene.Boolean()

    async def mutate(self, info, tenant=None, account_tag=None, transaction_tag=None):
        storage = storage_service.get(info.context["request"])
        ok = await account_service.rollback_transaction(
            storage, tenant, account_tag, transaction_tag
        )
        return commitAccountTransaction(ok=ok)


async def get_account(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    account_tag: Optional[str] = None,
):
    if id is None and not (tenant is not None and account_tag is not None):
        raise ValueError("Provide either the id or tenant and account_tag!")
    storage = storage_service.get(info.context["request"])
    account = await account_service.get(
        storage, id=id, tenant=tenant, account_tag=account_tag
    )
    return account


async def all_accounts(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    return await account_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_accounts_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    meta = await account_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}


async def get_account_transaction(
    info, tenant: str, account_tag: str, transaction_tag: str
):
    storage = storage_service.get(info.context["request"])
    return await account_service.get_transaction(
        storage, tenant, account_tag, transaction_tag
    )
