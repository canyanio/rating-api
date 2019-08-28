import re

from typing import List, Optional
from datetime import datetime
from uuid import uuid4
from pymongo import ASCENDING, DESCENDING  # type: ignore
from pymongo.collection import ReturnDocument  # type: ignore

from . import customer as customer_service
from .storage import StorageService


async def process(storage: StorageService, invoice: dict) -> dict:
    invoice = invoice.copy()
    #
    if invoice.get("customer_tag"):
        customer = await customer_service.get(
            storage,
            tenant=invoice.get("tenant"),
            customer_tag=invoice.get("customer_tag"),
        )
        if customer is None:
            raise ValueError(
                "Customer with id = %s not found in tenant %s!"
                % (invoice.get("customer_tag"), invoice.get("tenant"))
            )
        invoice["customer_tag"] = customer["customer_tag"]
    return invoice


async def serialize(storage: StorageService, result: dict) -> dict:
    result = await process(storage, result)
    return {
        "id": result.get("_id"),
        "tenant": result.get("tenant"),
        "invoice_number": result.get("invoice_number"),
        "invoice_date": result.get("invoice_date"),
        "customer_tag": result.get("customer_tag"),
        "customer": await customer_service.get(
            storage,
            tenant=result.get("tenant"),
            customer_tag=result.get("customer_tag"),
        )
        if result.get("customer_tag")
        else None,
        "rows": [
            {
                "prefix": item.get("prefix"),
                "description": item.get("description"),
                "unit_price": item.get("unit_price"),
                "quantity": item.get("quantity"),
                "total": item.get("total"),
            }
            for item in (result.get("rows") or ())
        ],
        "net_total": result.get("net_total"),
        "vat_rate": result.get("vat_rate"),
        "total": result.get("total"),
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    invoice_number: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "invoice_number": invoice_number}
    result = await storage.db["invoices"].find_one(params)
    return await serialize(storage, result) if result is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {
                        "invoice_number": re.compile(
                            re.escape(filter["q"]), re.IGNORECASE
                        )
                    },
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    if filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("invoice_number"):
        filters_and.append({"invoice_number": filter["invoice_number"]})
    if filter.get("invoice_date"):
        filters_and.append(
            {
                "invoice_date": datetime.combine(
                    filter["invoice_date"], datetime.min.time()
                )
            }
        )
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
    result = storage.db["invoices"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    invoices = [
        await serialize(storage, invoice)
        for invoice in await result.skip(page * perPage).limit(perPage).to_list(None)
    ]
    return invoices


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["invoices"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, invoice: dict) -> Optional[dict]:
    invoice = await process(storage, invoice)
    result = await storage.db["invoices"].find_one_and_update(
        {"_id": invoice.get("id")}
        if invoice.get("id")
        else {
            "tenant": invoice.get("tenant"),
            "invoice_number": invoice.get("invoice_number"),
        },
        {
            "$setOnInsert": {"_id": invoice.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": invoice.get("tenant"),
                    "invoice_number": invoice["invoice_number"],
                    "invoice_date": datetime.combine(
                        invoice["invoice_date"], datetime.min.time()
                    )
                    if invoice.get("invoice_date")
                    else None,
                    "customer_tag": invoice.get("customer_tag"),
                    "rows": [
                        {
                            "prefix": item.get("prefix"),
                            "description": item.get("description"),
                            "unit_price": item.get("unit_price"),
                            "quantity": item.get("quantity"),
                            "total": item.get("total"),
                        }
                        for item in (invoice.get("rows") or [])
                    ]
                    if invoice.get("rows") is not None
                    else None,
                    "net_total": invoice.get("net_total"),
                    "vat_rate": invoice.get("vat_rate"),
                    "total": invoice.get("total"),
                }
            ),
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return await serialize(storage, result) if result is not None else None


async def delete(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    invoice_number: Optional[str] = None,
) -> Optional[dict]:
    invoice = await get(
        storage, id=id, tenant=tenant, invoice_number=invoice_number, role="W"
    )
    if invoice is not None:
        await storage.db["invoices"].delete_one({"_id": invoice["id"]})
    return invoice
