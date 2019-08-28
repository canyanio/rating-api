from datetime import date
from typing import List, Optional

import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore

from .customer import Customer
from ..services import invoice as invoice_service
from ..services import storage as storage_service
from ..types import BigInt


class InvoiceFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    invoice_number = graphene.String()
    invoice_date = graphene.Date()
    customer_tag = graphene.String()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "invoice_number": self.invoice_number,
            "invoice_date": self.invoice_date,
            "customer_tag": self.customer_tag,
        }


class InvoiceRow(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    prefix = graphene.String()
    description = graphene.String()
    unit_price = graphene.Int()
    quantity = BigInt()
    total = BigInt()


class Invoice(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    invoice_number = graphene.String(required=True)
    invoice_date = graphene.Date(required=True)
    customer = graphene.Field(Customer)
    rows = graphene.List(InvoiceRow)
    net_total = BigInt()
    vat_rate = graphene.Int()
    total = BigInt()


class InputInvoiceRow(graphene.InputObjectType):
    prefix = graphene.String()
    description = graphene.String()
    unit_price = graphene.Int()
    quantity = BigInt()
    total = BigInt()


class upsertInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        invoice_number = graphene.String()
        invoice_date = graphene.Date()
        customer_tag = graphene.String()
        rows = graphene.List(InputInvoiceRow)
        net_total = BigInt()
        vat_rate = graphene.Int()
        total = BigInt()

    class Meta:
        default_resolver = dict_resolver

    Output = Invoice

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        invoice_number: Optional[str] = None,
        invoice_date: date = None,
        customer_tag: Optional[str] = None,
        rows: List[dict] = None,
        net_total: int = None,
        vat_rate: int = None,
        total: int = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and invoice_number is not None):
            raise ValueError("Provide either the id or tenant and invoice_number!")
        storage = storage_service.get(info.context["request"])
        return await invoice_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                invoice_number=invoice_number,
                invoice_date=invoice_date,
                customer_tag=customer_tag,
                rows=rows,
                net_total=net_total,
                vat_rate=vat_rate,
                total=total,
            ),
        )


class deleteInvoice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        invoice_number = graphene.String()

    Output = Invoice

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        invoice_number: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and invoice_number is not None):
            raise ValueError("Provide either the id or tenant and invoice_number!")
        storage = storage_service.get(info.context["request"])
        return await invoice_service.delete(
            storage, id=id, tenant=tenant, invoice_number=invoice_number
        )


async def get_invoice(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    invoice_number: Optional[str] = None,
) -> Optional[dict]:
    if id is None and not (tenant is not None and invoice_number is not None):
        raise ValueError("Provide either the id or tenant and invoice_number!")
    storage = storage_service.get(info.context["request"])
    return await invoice_service.get(
        storage, id=id, tenant=tenant, invoice_number=invoice_number
    )


async def all_invoices(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    storage = storage_service.get(info.context["request"])
    return await invoice_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_invoices_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    storage = storage_service.get(info.context["request"])
    meta = await invoice_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
