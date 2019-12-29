from typing import List, Optional

import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore

from ..services import seller as seller_service
from ..services import storage as storage_service


class SellerFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    seller_tag = graphene.String()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "seller_tag": self.seller_tag,
        }


class Seller(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    seller_tag = graphene.String(required=True)
    company_name = graphene.String()
    firstname = graphene.String()
    lastname = graphene.String()
    email = graphene.String()
    tax_number = graphene.String()
    vat_number = graphene.String()
    address = graphene.String()
    zipcode = graphene.String()
    city = graphene.String()
    province = graphene.String()
    country = graphene.String()
    active = graphene.Boolean()


class upsertSeller(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        seller_tag = graphene.String()
        company_name = graphene.String()
        firstname = graphene.String()
        lastname = graphene.String()
        email = graphene.String()
        tax_number = graphene.String()
        vat_number = graphene.String()
        address = graphene.String()
        zipcode = graphene.String()
        city = graphene.String()
        province = graphene.String()
        country = graphene.String()
        active = graphene.Boolean()

    class Meta:
        default_resolver = dict_resolver

    Output = Seller

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        seller_tag: Optional[str] = None,
        company_name: Optional[str] = None,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
        tax_number: Optional[str] = None,
        vat_number: Optional[str] = None,
        address: Optional[str] = None,
        zipcode: Optional[str] = None,
        city: Optional[str] = None,
        province: Optional[str] = None,
        country: Optional[str] = None,
        active: bool = True,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and seller_tag is not None):
            raise ValueError("Provide either the id or tenant and seller_tag!")
        storage = storage_service.get(info.context["request"])
        return await seller_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                seller_tag=seller_tag,
                company_name=company_name,
                firstname=firstname,
                lastname=lastname,
                email=email,
                tax_number=tax_number,
                vat_number=vat_number,
                address=address,
                zipcode=zipcode,
                city=city,
                province=province,
                country=country,
                active=active,
            ),
        )


class deleteSeller(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        seller_tag = graphene.String()

    Output = Seller

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        seller_tag: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and seller_tag is not None):
            raise ValueError("Provide either the id or tenant and seller_tag!")
        storage = storage_service.get(info.context["request"])
        return await seller_service.delete(
            storage, id=id, tenant=tenant, seller_tag=seller_tag
        )


async def get_seller(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    seller_tag: Optional[str] = None,
) -> Optional[dict]:
    if id is None and not (tenant is not None and seller_tag is not None):
        raise ValueError("Provide either the id or tenant and seller_tag!")
    storage = storage_service.get(info.context["request"])
    return await seller_service.get(
        storage, id=id, tenant=tenant, seller_tag=seller_tag
    )


async def all_sellers(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    storage = storage_service.get(info.context["request"])
    return await seller_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_sellers_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    storage = storage_service.get(info.context["request"])
    meta = await seller_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
