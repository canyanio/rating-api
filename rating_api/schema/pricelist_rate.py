import graphene  # type: ignore

from datetime import datetime
from typing import List, Optional

from graphene.types.resolver import dict_resolver  # type: ignore

from ..services import pricelist as pricelist_service
from ..services import storage as storage_service


class PricelistRateFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    pricelist_id = graphene.ID()
    pricelist_tag = graphene.String()
    carrier_id = graphene.ID()
    carrier_tag = graphene.String()
    prefix = graphene.String()
    active = graphene.Boolean()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "pricelist_id": self.pricelist_id,
            "pricelist_tag": self.pricelist_tag,
            "carrier_id": self.carrier_id,
            "carrier_tag": self.carrier_tag,
            "prefix": self.prefix,
            "active": self.active,
        }


class PricelistRate(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID()
    tenant = graphene.ID(required=True)
    pricelist_id = graphene.ID()
    pricelist_tag = graphene.String()
    carrier_id = graphene.ID()
    carrier_tag = graphene.String()
    prefix = graphene.String(required=True)
    datetime_start = graphene.DateTime()
    datetime_end = graphene.DateTime()
    active = graphene.Boolean(default_value=True)
    connect_fee = graphene.Int()
    rate = graphene.Int()
    rate_increment = graphene.Int()
    interval_start = graphene.Int()
    description = graphene.String()


class upsertPricelistRate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        pricelist_id = graphene.ID()
        pricelist_tag = graphene.String()
        carrier_id = graphene.ID()
        carrier_tag = graphene.String()
        prefix = graphene.String()
        datetime_start = graphene.DateTime()
        datetime_end = graphene.DateTime()
        active = graphene.Boolean(default_value=True)
        connect_fee = graphene.Int()
        rate = graphene.Int()
        rate_increment = graphene.Int()
        interval_start = graphene.Int()
        description = graphene.String()

    class Meta:
        default_resolver = dict_resolver

    Output = PricelistRate

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_id: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
        carrier_id: Optional[str] = None,
        carrier_tag: Optional[str] = None,
        prefix: Optional[str] = None,
        datetime_start: datetime = None,
        datetime_end: datetime = None,
        active: bool = None,
        connect_fee: int = None,
        rate: int = None,
        rate_increment: int = None,
        interval_start: int = None,
        description: Optional[str] = None,
    ):
        if id is None and not (
            (tenant is not None or pricelist_id is not None)
            and (pricelist_tag is not None or pricelist_id is not None)
            and (carrier_tag is not None or carrier_id is not None)
            and prefix is not None
        ):
            raise ValueError(
                "Provide either the id or tenant, pricelist_tag, carrier_tag and prefix!"
            )
        storage = storage_service.get(info.context["request"])
        return await pricelist_service.upsert_rate(
            storage,
            dict(
                id=id,
                tenant=tenant,
                pricelist_id=pricelist_id,
                pricelist_tag=pricelist_tag,
                carrier_id=carrier_id,
                carrier_tag=carrier_tag,
                prefix=prefix,
                datetime_start=datetime_start,
                datetime_end=datetime_end,
                active=active,
                connect_fee=connect_fee,
                rate=rate,
                rate_increment=rate_increment,
                interval_start=interval_start,
                description=description,
            ),
        )


class deletePricelistRate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        pricelist_tag = graphene.String()
        carrier_tag = graphene.String()
        prefix = graphene.String()

    Output = PricelistRate

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        pricelist_tag: Optional[str] = None,
        carrier_tag: Optional[str] = None,
        prefix: Optional[str] = None,
    ):
        if id is None and not (
            tenant is not None
            and pricelist_tag is not None
            and carrier_tag is not None
            and prefix is not None
        ):
            raise ValueError(
                "Provide either the id or tenant, pricelist_tag, carrier_tag and prefix!"
            )
        storage = storage_service.get(info.context["request"])
        return await pricelist_service.delete_rate(
            storage,
            id=id,
            tenant=tenant,
            pricelist_tag=pricelist_tag,
            carrier_tag=carrier_tag,
            prefix=prefix,
        )


async def get_pricelist_rate(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
    prefix: Optional[str] = None,
    carrier_tag: Optional[str] = None,
):
    if id is None and not (
        tenant is not None
        and pricelist_tag is not None
        and carrier_tag is not None
        and prefix is not None
    ):
        raise ValueError(
            "Provide either the id or tenant, pricelist_tag, carrier_tag and prefix!"
        )
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get_rate(
        storage,
        id=id,
        tenant=tenant,
        pricelist_tag=pricelist_tag,
        carrier_tag=carrier_tag,
        prefix=prefix,
    )


async def get_pricelist_rate_by_destination(
    info,
    tenant: Optional[str] = None,
    pricelist_tags: List[str] = None,
    carrier_tags: List[str] = None,
    carrier_tags_override: List[str] = None,
    destination: Optional[str] = None,
):
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get_rate_by_destination(
        storage,
        tenant=tenant,
        pricelist_tags=pricelist_tags,
        carrier_tags=carrier_tags,
        carrier_tags_override=carrier_tags_override,
        destination=destination,
    )


async def get_least_cost_routing(
    info,
    tenant: Optional[str] = None,
    carrier_tags: List[str] = None,
    carrier_tags_override: List[str] = None,
    destination: Optional[str] = None,
):
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get_least_cost_routing(
        storage,
        tenant=tenant,
        carrier_tags=carrier_tags,
        carrier_tags_override=carrier_tags_override,
        destination=destination,
    )


async def all_pricelist_rates(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    return await pricelist_service.get_all_rates(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_pricelist_rates_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
):
    storage = storage_service.get(info.context["request"])
    meta = await pricelist_service.get_all_rates_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
