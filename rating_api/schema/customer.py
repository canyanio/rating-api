from typing import List, Optional

import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore

from ..services import customer as customer_service
from ..services import storage as storage_service


class CustomerFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    customer_tag = graphene.String()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "customer_tag": self.customer_tag,
        }


class CustomerVATPolicy(graphene.Enum):
    EXEMPT = "EXEMPT"
    VAT_INCLUDED = "VAT_INCLUDED"
    VAT_EXCLUDED = "VAT_EXCLUDED"


class Customer(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    customer_tag = graphene.String(required=True)
    company_name = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    email = graphene.String()
    tax_number = graphene.String()
    vat_number = graphene.String()
    vat_policy = CustomerVATPolicy()
    address = graphene.String()
    zipcode = graphene.String()
    city = graphene.String()
    province = graphene.String()
    country = graphene.String()
    active = graphene.Boolean()


class upsertCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        customer_tag = graphene.String()
        company_name = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()
        email = graphene.String()
        tax_number = graphene.String()
        vat_number = graphene.String()
        vat_policy = CustomerVATPolicy()
        address = graphene.String()
        zipcode = graphene.String()
        city = graphene.String()
        province = graphene.String()
        country = graphene.String()
        active = graphene.Boolean()

    class Meta:
        default_resolver = dict_resolver

    Output = Customer

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        customer_tag: Optional[str] = None,
        company_name: Optional[str] = None,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        tax_number: Optional[str] = None,
        vat_number: Optional[str] = None,
        vat_policy: Optional[str] = None,
        address: Optional[str] = None,
        zipcode: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        country: Optional[str] = None,
        active: bool = True,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and customer_tag is not None):
            raise ValueError("Provide either the id or tenant and customer_tag!")
        storage = storage_service.get(info.context["request"])
        return await customer_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                customer_tag=customer_tag,
                company_name=company_name,
                firstname=firstname,
                lastname=lastname,
                email=email,
                tax_number=tax_number,
                vat_number=vat_number,
                vat_policy=vat_policy,
                address=address,
                zipcode=zipcode,
                city=city,
                province=province,
                country=country,
                active=active,
            ),
        )


class deleteCustomer(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        customer_tag = graphene.String()

    Output = Customer

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        customer_tag: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and customer_tag is not None):
            raise ValueError("Provide either the id or tenant and customer_tag!")
        storage = storage_service.get(info.context["request"])
        return await customer_service.delete(
            storage, id=id, tenant=tenant, customer_tag=customer_tag
        )


async def get_customer(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    customer_tag: Optional[str] = None,
) -> Optional[dict]:
    if id is None and not (tenant is not None and customer_tag is not None):
        raise ValueError("Provide either the id or tenant and customer_tag!")
    storage = storage_service.get(info.context["request"])
    return await customer_service.get(
        storage, id=id, tenant=tenant, customer_tag=customer_tag
    )


async def all_customers(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    storage = storage_service.get(info.context["request"])
    return await customer_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_customers_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    storage = storage_service.get(info.context["request"])
    meta = await customer_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
