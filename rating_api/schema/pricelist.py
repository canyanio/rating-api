from typing import List, Optional

import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore

from ..services import pricelist as pricelist_service
from ..services import storage as storage_service


class PricelistFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    pricelist_tag = graphene.String()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "pricelist_tag": self.pricelist_tag,
        }


class PricelistCurrency(graphene.Enum):
    EUR = "EUR"
    USD = "USD"


class Pricelist(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    pricelist_tag = graphene.String(required=True)
    name = graphene.String()
    currency = PricelistCurrency()


class upsertPricelist(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        pricelist_tag = graphene.String()
        name = graphene.String()
        currency = PricelistCurrency()

    class Meta:
        default_resolver = dict_resolver

    Output = Pricelist

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
        name: Optional[str] = None,
        currency: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and pricelist_tag is not None):
            raise ValueError("Provide either the id or tenant and pricelist_tag!")
        storage = storage_service.get(info.context["request"])
        return await pricelist_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                pricelist_tag=pricelist_tag,
                name=name,
                currency=currency,
            ),
        )


class deletePricelist(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        pricelist_tag = graphene.String()

    Output = Pricelist

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and pricelist_tag is not None):
            raise ValueError("Provide either the id or tenant and pricelist_tag!")
        storage = storage_service.get(info.context["request"])
        return await pricelist_service.delete(
            storage, id=id, tenant=tenant, pricelist_tag=pricelist_tag
        )


async def get_pricelist(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
) -> Optional[dict]:
    if id is None and not (tenant is not None and pricelist_tag is not None):
        raise ValueError("Provide either the id or tenant and pricelist_tag!")
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get(
        storage, id=id, tenant=tenant, pricelist_tag=pricelist_tag
    )


async def all_pricelists(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_pricelists_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    storage = storage_service.get(info.context["request"])
    meta = await pricelist_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
