import graphene  # type: ignore

from datetime import datetime
from typing import List, Optional

from graphene.types.resolver import dict_resolver  # type: ignore

from .account import Account, InputAccountPricelistRate
from .invoice import Invoice
from .pricelist_rate import PricelistRate
from ..services import storage as storage_service
from ..services import transaction as transaction_service


class TransactionFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    transaction_tag = graphene.String()
    account_tag = graphene.String()
    invoice_number = graphene.String()
    primary = graphene.Boolean()
    inbound = graphene.Boolean()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "transaction_tag": self.transaction_tag,
            "account_tag": self.account_tag,
            "invoice_number": self.invoice_number,
            "primary": self.primary,
            "inbound": self.inbound,
        }


class Transaction(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    transaction_tag = graphene.String(required=True)
    account_tag = graphene.String()
    account = graphene.Field(Account)
    invoice = graphene.Field(Invoice)
    source = graphene.String()
    source_ip = graphene.String()
    destination = graphene.String()
    carrier_ip = graphene.String()
    tags = graphene.List(graphene.String)
    authorized = graphene.Boolean()
    destination_rate = graphene.Field(PricelistRate)
    timestamp_auth = graphene.DateTime()
    timestamp_begin = graphene.DateTime()
    timestamp_end = graphene.DateTime()
    primary = graphene.Boolean()
    inbound = graphene.Boolean()
    failed = graphene.Boolean()
    failed_reason = graphene.String()
    duration = graphene.Int()
    fee = graphene.Int()


class upsertTransaction(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        transaction_tag = graphene.String()
        account_tag = graphene.String()
        invoice_number = graphene.String()
        source = graphene.String()
        source_ip = graphene.String()
        destination = graphene.String()
        carrier_ip = graphene.String()
        tags = graphene.List(graphene.String)
        authorized = graphene.Boolean()
        destination_rate = graphene.Argument(InputAccountPricelistRate)
        timestamp_auth = graphene.DateTime()
        timestamp_begin = graphene.DateTime()
        timestamp_end = graphene.DateTime()
        primary = graphene.Boolean()
        inbound = graphene.Boolean()
        failed = graphene.Boolean()
        failed_reason = graphene.String()
        duration = graphene.Int()
        fee = graphene.Int()

    class Meta:
        default_resolver = dict_resolver

    Output = Transaction

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        transaction_tag: Optional[str] = None,
        account_tag: Optional[str] = None,
        invoice_number: Optional[str] = None,
        source: Optional[str] = None,
        source_ip: Optional[str] = None,
        destination: Optional[str] = None,
        carrier_ip: Optional[str] = None,
        tags: List[str] = None,
        authorized: bool = None,
        destination_rate: Optional[str] = None,
        timestamp_auth: datetime = None,
        timestamp_begin: datetime = None,
        timestamp_end: datetime = None,
        inbound: bool = None,
        failed: bool = None,
        failed_reason: Optional[str] = None,
        duration: int = None,
        fee: int = None,
        primary: bool = None,
    ):
        if id is None and not (
            tenant is not None
            and transaction_tag is not None
            and account_tag is not None
        ):
            raise ValueError(
                "Provide either the id or tenant, transaction_tag and account_tag!"
            )
        storage = storage_service.get(info.context["request"])
        return await transaction_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                transaction_tag=transaction_tag,
                account_tag=account_tag,
                invoice_number=invoice_number,
                source=source,
                source_ip=source_ip,
                destination=destination,
                carrier_ip=carrier_ip,
                tags=tags,
                authorized=authorized,
                destination_rate=destination_rate,
                timestamp_auth=timestamp_auth,
                timestamp_begin=timestamp_begin,
                timestamp_end=timestamp_end,
                primary=primary,
                inbound=inbound,
                failed=failed,
                failed_reason=failed_reason,
                duration=duration,
                fee=fee,
            ),
        )


class deleteTransaction(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        transaction_tag = graphene.String()
        account_tag = graphene.String()

    class Meta:
        default_resolver = dict_resolver

    Output = Transaction

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        transaction_tag: Optional[str] = None,
        account_tag: Optional[str] = None,
    ):
        if id is None and not (
            tenant is not None
            and transaction_tag is not None
            and account_tag is not None
        ):
            raise ValueError(
                "Provide either the id or tenant, transaction_tag and account_tag!"
            )
        storage = storage_service.get(info.context["request"])
        return await transaction_service.delete(
            storage,
            id=id,
            tenant=tenant,
            transaction_tag=transaction_tag,
            account_tag=account_tag,
        )


async def get_transaction(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    transaction_tag: Optional[str] = None,
    account_tag: Optional[str] = None,
):
    if id is None and not (
        tenant is not None and transaction_tag is not None and account_tag is not None
    ):
        raise ValueError(
            "Provide either the id or tenant, transaction_tag and account_tag!"
        )
    storage = storage_service.get(info.context["request"])
    return await transaction_service.get(
        storage,
        id=id,
        tenant=tenant,
        transaction_tag=transaction_tag,
        account_tag=account_tag,
    )


async def all_transactions(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    return await transaction_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_transactions_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    meta = await transaction_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
