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
        "customer_tag": result.get("customer_tag"),
        "company_name": result.get("company_name"),
        "firstname": result.get("firstname"),
        "lastname": result.get("lastname"),
        "email": result.get("email"),
        "tax_number": result.get("tax_number"),
        "vat_number": result.get("vat_number"),
        "vat_policy": result.get("vat_policy"),
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
    customer_tag: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "customer_tag": customer_tag}
    result = await storage.db["customers"].find_one(params)
    return serialize(result) if result is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"customer_tag": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
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
    if filter.get("customer_tag"):
        filters_and.append({"customer_tag": filter["customer_tag"]})
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
    result = storage.db["customers"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    customers = list(
        serialize(customer)
        for customer in await result.skip(page * perPage).limit(perPage).to_list(None)
    )
    return customers


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["customers"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, customer: dict) -> Optional[dict]:
    result = await storage.db["customers"].find_one_and_update(
        {"_id": customer.get("id")}
        if customer.get("id")
        else {
            "tenant": customer.get("tenant"),
            "customer_tag": customer.get("customer_tag"),
        },
        {
            "$setOnInsert": {"_id": customer.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": customer.get("tenant"),
                    "customer_tag": customer["customer_tag"],
                    "company_name": customer.get("company_name"),
                    "firstname": customer.get("firstname"),
                    "lastname": customer.get("lastname"),
                    "email": customer.get("email"),
                    "tax_number": customer.get("tax_number"),
                    "vat_number": customer.get("vat_number"),
                    "vat_policy": customer.get("vat_policy"),
                    "address": customer.get("address"),
                    "zipcode": customer.get("zipcode"),
                    "city": customer.get("city"),
                    "province": customer.get("province"),
                    "country": customer.get("country"),
                    "active": bool(customer.get("active"))
                    if customer.get("active") is not None
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
    customer_tag: Optional[str] = None,
) -> Optional[dict]:
    customer = await get(
        storage, id=id, tenant=tenant, customer_tag=customer_tag, role="W"
    )
    if customer is not None:
        await storage.db["customers"].delete_one({"_id": customer["id"]})
    return customer
