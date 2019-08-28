import re

from typing import List, Optional
from operator import itemgetter
from uuid import uuid4
from pymongo import ASCENDING, DESCENDING  # type: ignore
from pymongo.collection import ReturnDocument  # type: ignore

from . import carrier as carrier_service
from .storage import StorageService


def serialize_pricelist(result: dict) -> dict:
    return {
        "id": result.get("_id"),
        "tenant": result.get("tenant"),
        "pricelist_tag": result.get("pricelist_tag"),
        "name": result.get("name"),
        "currency": result.get("currency"),
    }


async def process_pricelist_rate(storage: StorageService, pricelist_rate: dict) -> dict:
    pricelist_rate = pricelist_rate.copy()
    #
    if pricelist_rate.get("pricelist_id") or pricelist_rate.get("pricelist_tag"):
        pricelist = await get(
            storage,
            id=pricelist_rate.get("pricelist_id"),
            tenant=pricelist_rate.get("tenant"),
            pricelist_tag=pricelist_rate.get("pricelist_tag"),
        )
        if pricelist is None:
            raise ValueError(
                "Price list with id = %s and tag = %s not found in tenant %s!"
                % (
                    pricelist_rate.get("pricelist_id"),
                    pricelist_rate.get("pricelist_tag"),
                    pricelist_rate.get("tenant"),
                )
            )
        pricelist_rate["tenant"] = pricelist["tenant"]
        pricelist_rate["pricelist_id"] = pricelist["id"]
        pricelist_rate["pricelist_tag"] = pricelist["pricelist_tag"]
    #
    if pricelist_rate.get("carrier_id") or pricelist_rate.get("carrier_tag"):
        carrier = await carrier_service.get(
            storage,
            id=pricelist_rate.get("carrier_id"),
            tenant=pricelist_rate.get("tenant"),
            carrier_tag=pricelist_rate.get("carrier_tag"),
        )
        if carrier is None:
            raise ValueError(
                "Carrier with id = %s and tag = %s not found in tenant %s!"
                % (
                    pricelist_rate.get("carrier_id"),
                    pricelist_rate.get("carrier_tag"),
                    pricelist_rate.get("tenant"),
                )
            )
        pricelist_rate["carrier_id"] = carrier["id"]
        pricelist_rate["carrier_tag"] = carrier["carrier_tag"]
    return pricelist_rate


async def serialize_pricelist_rate(
    storage: StorageService, pricelist_rate: dict
) -> dict:
    pricelist_rate = await process_pricelist_rate(storage, pricelist_rate)
    return {
        "id": pricelist_rate.get("_id"),
        "tenant": pricelist_rate.get("tenant"),
        "pricelist_id": pricelist_rate.get("pricelist_id"),
        "pricelist_tag": pricelist_rate.get("pricelist_tag"),
        "carrier_id": pricelist_rate.get("carrier_id"),
        "carrier_tag": pricelist_rate.get("carrier_tag"),
        "prefix": pricelist_rate.get("prefix"),
        "datetime_start": pricelist_rate.get("datetime_start"),
        "datetime_end": pricelist_rate.get("datetime_end"),
        "active": bool(pricelist_rate.get("active"))
        if pricelist_rate.get("active") is not None
        else None,
        "connect_fee": pricelist_rate.get("connect_fee"),
        "rate": pricelist_rate.get("rate"),
        "rate_increment": pricelist_rate.get("rate_increment"),
        "interval_start": pricelist_rate.get("interval_start"),
        "description": pricelist_rate.get("description"),
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
    role="R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "pricelist_tag": pricelist_tag}
    result = await storage.db["pricelists"].find_one(params)
    return serialize_pricelist(result) if result is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {
                        "pricelist_tag": re.compile(
                            re.escape(filter["q"]), re.IGNORECASE
                        )
                    },
                    {"name": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    elif filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("pricelist_tag"):
        filters_and.append({"pricelist_tag": filter["pricelist_tag"]})
    return {"$and": filters_and} if filters_and else {}


async def get_all(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    query = await get_query(storage, filter)
    result = storage.db["pricelists"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    pricelists = list(
        serialize_pricelist(pricelist)
        for pricelist in await result.skip(page * perPage).limit(perPage).to_list(None)
    )
    return pricelists


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["pricelists"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, pricelist: dict) -> Optional[dict]:
    result = await storage.db["pricelists"].find_one_and_update(
        {"_id": pricelist.get("id")}
        if pricelist.get("id")
        else {
            "tenant": pricelist.get("tenant"),
            "pricelist_tag": pricelist.get("pricelist_tag"),
        },
        {
            "$setOnInsert": {"_id": pricelist.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": pricelist["tenant"],
                    "pricelist_tag": pricelist["pricelist_tag"],
                    "name": pricelist.get("name"),
                    "currency": pricelist.get("currency"),
                    "active": bool(pricelist.get("active"))
                    if pricelist.get("active") is not None
                    else None,
                }
            ),
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return serialize_pricelist(result) if result is not None else None


async def delete(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
) -> Optional[dict]:
    pricelist = await get(
        storage, id=id, tenant=tenant, pricelist_tag=pricelist_tag, role="W"
    )
    if pricelist is not None:
        await storage.db["pricelists"].delete_one({"_id": pricelist["id"]})
    return pricelist


async def get_rate(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
    carrier_tag: Optional[str] = None,
    prefix: Optional[str] = None,
    role="R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {
            "tenant": tenant,
            "pricelist_tag": pricelist_tag,
            "carrier_tag": carrier_tag,
            "prefix": prefix,
        }
    result = await storage.db["pricelist_rates"].find_one(params)
    return (
        await serialize_pricelist_rate(storage, result) if result is not None else None
    )


async def get_rates_query(
    storage: StorageService, filter: Optional[dict] = None
) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {
                        "pricelist_tag": re.compile(
                            re.escape(filter["q"]), re.IGNORECASE
                        )
                    },
                    {"prefix": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"description": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    if filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("carrier_tag"):
        filters_and.append({"carrier_tag": filter["carrier_tag"]})
    elif filter.get("carrier_id"):
        carrier = await carrier_service.get(storage, id=filter["carrier_id"])
        if carrier is not None:
            filters_and.append({"tenant": carrier["tenant"]})
            filters_and.append({"carrier_tag": carrier["carrier_tag"]})
    if filter.get("pricelist_tag"):
        filters_and.append({"pricelist_tag": filter["pricelist_tag"]})
    elif filter.get("pricelist_id"):
        pricelist = await get(storage, id=filter["pricelist_id"])
        if pricelist is not None:
            filters_and.append({"tenant": pricelist["tenant"]})
            filters_and.append({"pricelist_tag": pricelist["pricelist_tag"]})
    if filter.get("prefix"):
        filters_and.append({"prefix": filter["prefix"]})
    if filter.get("active"):
        filters_and.append({"active": filter["active"]})
    return {"$and": filters_and} if filters_and else {}


async def get_all_rates(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> List[dict]:
    query = await get_rates_query(storage, filter)
    result = storage.db["pricelist_rates"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "pricelist_rate_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    pricelist_rates = [
        await serialize_pricelist_rate(storage, pricelist_rate)
        for pricelist_rate in await result.skip(page * perPage)
        .limit(perPage)
        .to_list(None)
    ]
    return pricelist_rates


async def get_all_rates_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_rates_query(storage, filter)
    result = await storage.db["pricelist_rates"].count_documents(query)
    return {"count": result}


async def upsert_rate(storage: StorageService, pricelist_rate: dict) -> Optional[dict]:
    pricelist_rate = await process_pricelist_rate(storage, pricelist_rate)
    result = await storage.db["pricelist_rates"].find_one_and_update(
        {"_id": pricelist_rate.get("id")}
        if pricelist_rate.get("id")
        else {
            "tenant": pricelist_rate.get("tenant"),
            "pricelist_tag": pricelist_rate.get("pricelist_tag"),
            "carrier_tag": pricelist_rate.get("carrier_tag"),
            "prefix": pricelist_rate.get("prefix"),
        },
        {
            "$setOnInsert": {"_id": pricelist_rate.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": pricelist_rate.get("tenant"),
                    "pricelist_tag": pricelist_rate.get("pricelist_tag"),
                    "carrier_tag": pricelist_rate.get("carrier_tag"),
                    "prefix": pricelist_rate.get("prefix"),
                    "datetime_start": pricelist_rate.get("datetime_start"),
                    "datetime_end": pricelist_rate.get("datetime_end"),
                    "active": bool(pricelist_rate.get("active"))
                    if pricelist_rate.get("active") is not None
                    else None,
                    "connect_fee": pricelist_rate.get("connect_fee"),
                    "rate": pricelist_rate.get("rate"),
                    "rate_increment": pricelist_rate.get("rate_increment"),
                    "interval_start": pricelist_rate.get("interval_start"),
                    "description": pricelist_rate.get("description"),
                }
            ),
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return (
        await serialize_pricelist_rate(storage, result) if result is not None else None
    )


async def delete_rate(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    pricelist_tag: Optional[str] = None,
    carrier_tag: Optional[str] = None,
    prefix: Optional[str] = None,
) -> Optional[dict]:
    pricelist_rate = await get_rate(
        storage,
        id=id,
        tenant=tenant,
        pricelist_tag=pricelist_tag,
        carrier_tag=carrier_tag,
        prefix=prefix,
        role="W",
    )
    if pricelist_rate is not None:
        await storage.db["pricelist_rates"].delete_one({"_id": pricelist_rate["id"]})
    return pricelist_rate


async def get_rate_by_destination(
    storage: StorageService,
    tenant: Optional[str] = None,
    pricelist_tags: List[str] = None,
    carrier_tags: List[str] = None,
    carrier_tags_override: List[str] = None,
    destination: Optional[str] = None,
) -> Optional[dict]:
    destination = destination if destination is not None else ""
    prefixes = [destination[:i] for i in range(1, min(10, len(destination)))]
    results = (
        await storage.db["pricelist_rates"]
        .find(
            storage.filter_dict(
                {
                    "tenant": tenant,
                    "pricelist_tag": {"$in": pricelist_tags}
                    if pricelist_tags
                    else None,
                    "carrier_tag": {"$in": carrier_tags} if carrier_tags else None,
                    "prefix": {"$in": prefixes},
                    "active": True,
                }
            )
        )
        .to_list(None)
    )
    results = list(results)
    results.sort(key=lambda x: len(x["prefix"]), reverse=True)
    return await serialize_pricelist_rate(storage, results[0]) if len(results) else None


async def get_least_cost_routing(
    storage: StorageService,
    tenant: Optional[str] = None,
    carrier_tags: List[str] = None,
    carrier_tags_override: List[str] = None,
    destination: Optional[str] = None,
) -> List[dict]:
    destination = destination if destination is not None else ""
    prefixes = [destination[:i] for i in range(1, min(10, len(destination)))]
    params = {"tenant": tenant, "prefix": {"$in": prefixes}, "active": True}
    if carrier_tags is not None:
        params["carrier_tag"] = {"$in": carrier_tags}
    results = (
        await storage.db["pricelist_rates"]
        .find(storage.filter_dict(params))
        .to_list(None)
    )
    results.sort(key=itemgetter("rate"))
    return list(
        filter(
            None,
            [
                await carrier_service.get(
                    storage, tenant=tenant, carrier_tag=result["carrier_tag"]
                )
                for result in results
            ],
        )
    )
