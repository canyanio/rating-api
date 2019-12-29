from typing import List, Optional

import graphene  # type: ignore

from graphene.types.resolver import dict_resolver  # type: ignore

from ..services import carrier as carrier_service
from ..services import storage as storage_service


class CarrierFilter(graphene.InputObjectType):
    q = graphene.String()
    id = graphene.ID()
    ids = graphene.List(graphene.ID)
    tenant = graphene.ID(default_value='default')
    carrier_tag = graphene.String()

    def to_dict(self):
        return {
            "q": self.q,
            "id": self.id,
            "ids": self.ids,
            "tenant": self.tenant,
            "carrier_tag": self.carrier_tag,
        }


class CarrierProtocol(graphene.Enum):
    TCP = "TCP"
    UDP = "UDP"


class Carrier(graphene.ObjectType):
    class Meta:
        default_resolver = dict_resolver

    id = graphene.ID(required=True)
    tenant = graphene.ID(required=True)
    carrier_tag = graphene.String(required=True)
    host = graphene.String()
    port = graphene.Int()
    protocol = CarrierProtocol()
    active = graphene.Boolean(default_value=True)


class upsertCarrier(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        carrier_tag = graphene.String()
        host = graphene.String()
        port = graphene.Int()
        protocol = CarrierProtocol()
        active = graphene.Boolean(default_value=True)

    class Meta:
        default_resolver = dict_resolver

    Output = Carrier

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        carrier_tag: Optional[str] = None,
        host: Optional[str] = None,
        port: int = None,
        protocol: Optional[str] = None,
        active: bool = True,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and carrier_tag is not None):
            raise ValueError("Provide either the id or tenant and carrier_tag!")
        storage = storage_service.get(info.context["request"])
        return await carrier_service.upsert(
            storage,
            dict(
                id=id,
                tenant=tenant,
                carrier_tag=carrier_tag,
                host=host,
                port=port,
                protocol=protocol,
                active=active,
            ),
        )


class deleteCarrier(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        tenant = graphene.ID(default_value='default')
        carrier_tag = graphene.String()

    Output = Carrier

    async def mutate(
        self,
        info,
        id: Optional[str] = None,
        tenant: Optional[str] = None,
        carrier_tag: Optional[str] = None,
    ) -> Optional[dict]:
        if id is None and not (tenant is not None and carrier_tag is not None):
            raise ValueError("Provide either the id or tenant and carrier_tag!")
        storage = storage_service.get(info.context["request"])
        return await carrier_service.delete(
            storage, id=id, tenant=tenant, carrier_tag=carrier_tag
        )


async def get_carrier(
    info,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    carrier_tag: Optional[str] = None,
) -> Optional[dict]:
    if id is None and not (tenant is not None and carrier_tag is not None):
        raise ValueError("Provide either the id or tenant and carrier_tag!")
    storage = storage_service.get(info.context["request"])
    return await carrier_service.get(
        storage, id=id, tenant=tenant, carrier_tag=carrier_tag
    )


async def all_carriers(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    storage = storage_service.get(info.context["request"])
    return await carrier_service.get_all(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )


async def all_carriers_meta(
    info,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    storage = storage_service.get(info.context["request"])
    meta = await carrier_service.get_all_meta(
        storage,
        page=page,
        perPage=perPage,
        sortField=sortField,
        sortOrder=sortOrder,
        filter=filter,
    )
    return {"count": meta["count"]}
