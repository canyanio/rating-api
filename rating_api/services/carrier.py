import re

from typing import List, Optional
from uuid import uuid4
from pymongo import ASCENDING, DESCENDING  # type: ignore
from pymongo.collection import ReturnDocument  # type: ignore

from .storage import StorageService


def serialize(result: dict) -> dict:
    return {
        "id": result.get("_id"),
        "tenant": result.get("tenant"),
        "carrier_tag": result.get("carrier_tag"),
        "host": result.get("host"),
        "port": result.get("port"),
        "protocol": result.get("protocol"),
        "active": bool(result.get("active"))
        if result.get("active") is not None
        else None,
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    carrier_tag: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "carrier_tag": carrier_tag}
    result = await storage.db["carriers"].find_one(params)
    return serialize(result) if result is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"carrier_tag": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"host": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
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
    result = storage.db["carriers"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    carriers = list(
        serialize(carrier)
        for carrier in await result.skip(page * perPage).limit(perPage).to_list(None)
    )
    return carriers


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["carriers"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, carrier: dict) -> Optional[dict]:
    result = await storage.db["carriers"].find_one_and_update(
        {"_id": carrier.get("id")}
        if carrier.get("id")
        else {
            "tenant": carrier.get("tenant"),
            "carrier_tag": carrier.get("carrier_tag"),
        },
        {
            "$setOnInsert": {"_id": carrier.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": carrier.get("tenant"),
                    "carrier_tag": carrier["carrier_tag"],
                    "host": carrier.get("host"),
                    "port": carrier.get("port"),
                    "protocol": carrier.get("protocol"),
                    "active": bool(carrier.get("active"))
                    if carrier.get("active") is not None
                    else None,
                }
            ),
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return serialize(result) if result is not None else None


async def delete(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    carrier_tag: Optional[str] = None,
) -> Optional[dict]:
    carrier = await get(
        storage, id=id, tenant=tenant, carrier_tag=carrier_tag, role="W"
    )
    if carrier is not None:
        await storage.db["carriers"].delete_one({"_id": carrier["id"]})
    return carrier
