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
        "seller_tag": result.get("seller_tag"),
        "company_name": result.get("company_name"),
        "firstname": result.get("firstname"),
        "lastname": result.get("lastname"),
        "email": result.get("email"),
        "tax_number": result.get("tax_number"),
        "vat_number": result.get("vat_number"),
        "address": result.get("address"),
        "zipcode": result.get("zipcode"),
        "city": result.get("city"),
        "province": result.get("province"),
        "country": result.get("country"),
        "active": bool(result.get("active"))
        if result.get("active") is not None
        else None,
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    seller_tag: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "seller_tag": seller_tag}
    result = await storage.db["sellers"].find_one(params)
    return serialize(result) if result is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"seller_tag": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"company_name": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"tax_number": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"vat_number": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    if filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("seller_tag"):
        filters_and.append({"seller_tag": filter["seller_tag"]})
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
    result = storage.db["sellers"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    sellers = list(
        serialize(seller)
        for seller in await result.skip(page * perPage).limit(perPage).to_list(None)
    )
    return sellers


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["sellers"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, seller: dict) -> Optional[dict]:
    result = await storage.db["sellers"].find_one_and_update(
        {"_id": seller.get("id")}
        if seller.get("id")
        else {"tenant": seller.get("tenant"), "seller_tag": seller.get("seller_tag")},
        {
            "$setOnInsert": {"_id": seller.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": seller.get("tenant"),
                    "seller_tag": seller["seller_tag"],
                    "company_name": seller.get("company_name"),
                    "firstname": seller.get("firstname"),
                    "lastname": seller.get("lastname"),
                    "email": seller.get("email"),
                    "tax_number": seller.get("tax_number"),
                    "vat_number": seller.get("vat_number"),
                    "address": seller.get("address"),
                    "zipcode": seller.get("zipcode"),
                    "city": seller.get("city"),
                    "province": seller.get("province"),
                    "country": seller.get("country"),
                    "active": bool(seller.get("active"))
                    if seller.get("active") is not None
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
    seller_tag: Optional[str] = None,
) -> Optional[dict]:
    seller = await get(storage, id=id, tenant=tenant, seller_tag=seller_tag, role="W")
    if seller is not None:
        await storage.db["sellers"].delete_one({"_id": seller["id"]})
    return seller
