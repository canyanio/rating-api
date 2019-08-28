import graphene  # type: ignore

from typing import Optional

from .meta import ListMetadata

from .account import (
    Account as AccountType,
    AccountTransaction,
    AccountFilter,
    get_account,
    get_account_transaction,
    all_accounts,
    all_accounts_meta,
    upsertAccount,
    deleteAccount,
    beginAccountTransaction,
    endAccountTransaction,
    commitAccountTransaction,
    rollbackAccountTransaction,
    incrementAccountBalance,
    setAccountBalance,
)

from .carrier import (
    Carrier as CarrierType,
    CarrierFilter,
    get_carrier,
    all_carriers,
    all_carriers_meta,
    upsertCarrier,
    deleteCarrier,
)

from .customer import (
    Customer as CustomerType,
    CustomerFilter,
    get_customer,
    all_customers,
    all_customers_meta,
    upsertCustomer,
    deleteCustomer,
)

from .seller import (
    Seller as SellerType,
    SellerFilter,
    get_seller,
    all_sellers,
    all_sellers_meta,
    upsertSeller,
    deleteSeller,
)

from .invoice import (
    Invoice as InvoiceType,
    InvoiceFilter,
    get_invoice,
    all_invoices,
    all_invoices_meta,
    upsertInvoice,
    deleteInvoice,
)

from .pricelist import (
    Pricelist as PricelistType,
    PricelistFilter,
    get_pricelist,
    all_pricelists,
    all_pricelists_meta,
    upsertPricelist,
    deletePricelist,
)

from .pricelist_rate import (
    PricelistRate as PricelistRateType,
    PricelistRateFilter,
    get_pricelist_rate,
    all_pricelist_rates,
    all_pricelist_rates_meta,
    upsertPricelistRate,
    deletePricelistRate,
    get_least_cost_routing,
)

from .transaction import (
    Transaction as TransactionType,
    TransactionFilter,
    get_transaction,
    all_transactions,
    all_transactions_meta,
    upsertTransaction,
    deleteTransaction,
)


class Query(graphene.ObjectType):
    # carriers
    carrier = graphene.Field(
        lambda: CarrierType,
        name="Carrier",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        carrier_tag=graphene.String(),
    )
    all_carriers = graphene.List(
        lambda: CarrierType,
        name="allCarriers",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=CarrierFilter(),
    )
    all_carriers_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allCarriersMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=CarrierFilter(),
    )

    async def resolve_carrier(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        carrier_tag: Optional[str] = None,
    ):
        return get_carrier(info, id=id, tenant=tenant, carrier_tag=carrier_tag)

    async def resolve_all_carriers(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: CarrierFilter = None,
    ):
        return all_carriers(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_carriers_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: CarrierFilter = None,
    ):
        return all_carriers_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # customers
    customer = graphene.Field(
        lambda: CustomerType,
        name="Customer",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        customer_tag=graphene.String(),
    )
    all_customers = graphene.List(
        lambda: CustomerType,
        name="allCustomers",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=CustomerFilter(),
    )
    all_customers_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allCustomersMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=CustomerFilter(),
    )

    async def resolve_customer(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        customer_tag: Optional[str] = None,
    ):
        return get_customer(info, id=id, tenant=tenant, customer_tag=customer_tag)

    async def resolve_all_customers(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: CustomerFilter = None,
    ):
        return all_customers(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_customers_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: CustomerFilter = None,
    ):
        return all_customers_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # sellers
    seller = graphene.Field(
        lambda: SellerType,
        name="Seller",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        seller_tag=graphene.String(),
    )
    all_sellers = graphene.List(
        lambda: SellerType,
        name="allSellers",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=SellerFilter(),
    )
    all_sellers_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allSellersMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=SellerFilter(),
    )

    async def resolve_seller(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        seller_tag: Optional[str] = None,
    ):
        return get_seller(info, id=id, tenant=tenant, seller_tag=seller_tag)

    async def resolve_all_sellers(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: SellerFilter = None,
    ):
        return all_sellers(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_sellers_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: SellerFilter = None,
    ):
        return all_sellers_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # invoices
    invoice = graphene.Field(
        lambda: InvoiceType,
        name="Invoice",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        invoice_number=graphene.String(),
    )
    all_invoices = graphene.List(
        lambda: InvoiceType,
        name="allInvoices",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=InvoiceFilter(),
    )
    all_invoices_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allInvoicesMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=InvoiceFilter(),
    )

    async def resolve_invoice(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        invoice_number: Optional[str] = None,
    ):
        return get_invoice(info, id=id, tenant=tenant, invoice_number=invoice_number)

    async def resolve_all_invoices(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: InvoiceFilter = None,
    ):
        return all_invoices(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_invoices_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: InvoiceFilter = None,
    ):
        return all_invoices_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # pricelists
    pricelist = graphene.Field(
        lambda: PricelistType,
        name="Pricelist",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        pricelist_tag=graphene.String(),
    )
    all_pricelists = graphene.List(
        lambda: PricelistType,
        name="allPricelists",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=PricelistFilter(),
    )
    all_pricelists_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allPricelistsMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=PricelistFilter(),
    )

    async def resolve_pricelist(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
    ):
        return get_pricelist(info, id=id, tenant=tenant, pricelist_tag=pricelist_tag)

    async def resolve_all_pricelists(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: PricelistFilter = None,
    ):
        return all_pricelists(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_pricelists_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: PricelistFilter = None,
    ):
        return all_pricelists_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # pricelist_rates
    pricelist_rate = graphene.Field(
        lambda: PricelistRateType,
        name="PricelistRate",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        pricelist_tag=graphene.String(),
        prefix=graphene.String(),
        carrier_tag=graphene.String(),
    )
    all_pricelist_rates = graphene.List(
        lambda: PricelistRateType,
        name="allPricelistRates",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=PricelistRateFilter(),
    )
    all_pricelist_rates_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allPricelistRatesMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=PricelistRateFilter(),
    )

    async def resolve_pricelist_rate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
        prefix: Optional[str] = None,
        carrier_tag: Optional[str] = None,
    ):
        return get_pricelist_rate(
            info,
            id=id,
            tenant=tenant,
            pricelist_tag=pricelist_tag,
            prefix=prefix,
            carrier_tag=carrier_tag,
        )

    async def resolve_all_pricelist_rates(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: PricelistRateFilter = None,
    ):
        return all_pricelist_rates(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_pricelist_rates_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: PricelistRateFilter = None,
    ):
        return all_pricelist_rates_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # accounts
    account = graphene.Field(
        lambda: AccountType,
        name="Account",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        account_tag=graphene.String(),
    )
    account_transaction = graphene.Field(
        lambda: AccountTransaction,
        name="AccountTransaction",
        tenant=graphene.ID(default_value='default'),
        account_tag=graphene.String(),
        transaction_tag=graphene.String(),
    )
    all_accounts = graphene.List(
        lambda: AccountType,
        name="allAccounts",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=AccountFilter(),
    )
    all_accounts_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allAccountsMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=AccountFilter(),
    )

    async def resolve_account(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        account_tag: Optional[str] = None,
    ):
        return get_account(info, id=id, tenant=tenant, account_tag=account_tag)

    async def resolve_account_transaction(
        self, info, tenant=None, account_tag=None, transaction_tag=None
    ):
        return get_account_transaction(info, tenant, account_tag, transaction_tag)

    async def resolve_all_accounts(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: AccountFilter = None,
    ):
        return all_accounts(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_accounts_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: AccountFilter = None,
    ):
        return all_accounts_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # transactions
    transaction = graphene.Field(
        lambda: TransactionType,
        name="Transaction",
        id=graphene.ID(),
        tenant=graphene.ID(default_value='default'),
        transaction_tag=graphene.String(),
        account_tag=graphene.String(),
    )
    all_transactions = graphene.List(
        lambda: TransactionType,
        name="allTransactions",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=TransactionFilter(),
    )
    all_transactions_meta = graphene.Field(
        lambda: ListMetadata,
        name="_allTransactionsMeta",
        page=graphene.Int(),
        perPage=graphene.Int(),
        sortField=graphene.String(),
        sortOrder=graphene.String(),
        filter=TransactionFilter(),
    )

    async def resolve_transaction(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        transaction_tag: Optional[str] = None,
        account_tag: Optional[str] = None,
    ):
        return get_transaction(
            info,
            id=id,
            tenant=tenant,
            transaction_tag=transaction_tag,
            account_tag=account_tag,
        )

    async def resolve_all_transactions(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: TransactionFilter = None,
    ):
        return all_transactions(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    async def resolve_all_transactions_meta(
        self,
        info,
        page: int = 0,
        perPage: int = 25,
        sortField: str = "id",
        sortOrder: str = "asc",
        filter: TransactionFilter = None,
    ):
        return all_transactions_meta(
            info,
            page=page,
            perPage=perPage,
            sortField=sortField,
            sortOrder=sortOrder,
            filter=filter.to_dict() if filter is not None else None,
        )

    # additional API query end-points
    least_cost_routing = graphene.List(
        CarrierType,
        name="leastCostRouting",
        tenant=graphene.ID(default_value='default'),
        carrier_tags=graphene.List(graphene.String),
        carrier_tags_override=graphene.List(graphene.String),
        destination=graphene.String(),
    )

    async def resolve_least_cost_routing(
        self,
        info,
        tenant=None,
        carrier_tags=None,
        carrier_tags_override=None,
        destination=None,
    ):
        return get_least_cost_routing(
            info,
            tenant=tenant,
            carrier_tags=carrier_tags,
            carrier_tags_override=carrier_tags_override,
            destination=destination,
        )


class Mutations(graphene.ObjectType):
    # carriers
    create_carrier = upsertCarrier.Field(name="createCarrier")
    update_carrier = upsertCarrier.Field(name="updateCarrier")
    upsert_carrier = upsertCarrier.Field(name="upsertCarrier")
    delete_carrier = deleteCarrier.Field(name="deleteCarrier")

    # customers
    create_customer = upsertCustomer.Field(name="createCustomer")
    update_customer = upsertCustomer.Field(name="updateCustomer")
    upsert_customer = upsertCustomer.Field(name="upsertCustomer")
    delete_customer = deleteCustomer.Field(name="deleteCustomer")

    # sellers
    create_seller = upsertSeller.Field(name="createSeller")
    update_seller = upsertSeller.Field(name="updateSeller")
    upsert_seller = upsertSeller.Field(name="upsertSeller")
    delete_seller = deleteSeller.Field(name="deleteSeller")

    # invoices
    create_invoice = upsertInvoice.Field(name="createInvoice")
    update_invoice = upsertInvoice.Field(name="updateInvoice")
    upsert_invoice = upsertInvoice.Field(name="upsertInvoice")
    delete_invoice = deleteInvoice.Field(name="deleteInvoice")

    # pricelists
    create_pricelist = upsertPricelist.Field(name="createPricelist")
    update_pricelist = upsertPricelist.Field(name="updatePricelist")
    upsert_pricelist = upsertPricelist.Field(name="upsertPricelist")
    delete_pricelist = deletePricelist.Field(name="deletePricelist")

    # pricelist_rats
    create_pricelist_rate = upsertPricelistRate.Field(name="createPricelistRate")
    update_pricelist_rate = upsertPricelistRate.Field(name="updatePricelistRate")
    upsert_pricelist_rate = upsertPricelistRate.Field(name="upsertPricelistRate")
    delete_pricelist_rate = deletePricelistRate.Field(name="deletePricelistRate")

    # accounts
    create_account = upsertAccount.Field(name="createAccount")
    update_account = upsertAccount.Field(name="updateAccount")
    upsert_account = upsertAccount.Field(name="upsertAccount")
    delete_account = deleteAccount.Field(name="deleteAccount")
    begin_account_transaction = beginAccountTransaction.Field(
        name="beginAccountTransaction"
    )
    end_account_transaction = endAccountTransaction.Field(name="endAccountTransaction")
    commit_account_transaction = commitAccountTransaction.Field(
        name="commitAccountTransaction"
    )
    rollback_account_transaction = rollbackAccountTransaction.Field(
        name="rollbackAccountTransaction"
    )
    increment_account_balance = incrementAccountBalance.Field(
        name="incrementAccountBalance"
    )
    set_account_balance = setAccountBalance.Field(name="setAccountBalance")

    # transactions
    create_transaction = upsertTransaction.Field(name="createTransaction")
    update_transaction = upsertTransaction.Field(name="updateTransaction")
    upsert_transaction = upsertTransaction.Field(name="upsertTransaction")
    delete_transaction = deleteTransaction.Field(name="deleteTransaction")


schema = graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False)
