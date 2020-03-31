import re

from typing import List, Optional
from uuid import uuid4
from pymongo import ASCENDING, DESCENDING  # type: ignore
from pymongo.collection import ReturnDocument  # type: ignore

from . import account as account_service
from . import invoice as invoice_service
from .storage import StorageService


async def process(storage: StorageService, transaction: dict) -> dict:
    transaction = transaction.copy()
    #
    if transaction.get("account_tag"):
        account = await account_service.get(
            storage,
            tenant=transaction.get("tenant"),
            account_tag=transaction.get("account_tag"),
        )
        if account is None:
            raise ValueError(
                "Account with id = %s not found in tenant %s!"
                % (transaction.get("account_tag"), transaction.get("tenant"))
            )
        transaction["account"] = account
        transaction["account_tag"] = account["account_tag"]
    #
    if transaction.get("invoice_number"):
        invoice = await invoice_service.get(
            storage,
            tenant=transaction.get("tenant"),
            invoice_number=transaction.get("invoice_number"),
        )
        if invoice is None:
            raise ValueError(
                "Invoice with number = %s not found in tenant %s!"
                % (transaction.get("invoice_number"), transaction.get("tenant"))
            )
        transaction["invoice"] = invoice
        transaction["invoice_number"] = invoice["invoice_number"]
    return transaction


async def serialize(storage: StorageService, transaction: dict) -> dict:
    transaction = await process(storage, transaction)
    return {
        "id": transaction.get("_id"),
        "tenant": transaction.get("tenant"),
        "transaction_tag": transaction.get("transaction_tag"),
        "account": transaction.get("account"),
        "account_tag": transaction.get("account_tag"),
        "invoice": transaction.get("invoice"),
        "source": transaction.get("source"),
        "source_ip": transaction.get("source_ip"),
        "carrier_ip": transaction.get("carrier_ip"),
        "destination": transaction.get("destination"),
        "destination_rate": transaction.get("destination_rate"),
        "tags": transaction.get("tags"),
        "authorized": transaction.get("authorized"),
        "timestamp_auth": transaction.get("timestamp_auth"),
        "timestamp_begin": transaction.get("timestamp_begin"),
        "timestamp_end": transaction.get("timestamp_end"),
        "primary": transaction.get("primary"),
        "inbound": transaction.get("inbound"),
        "duration": transaction.get("duration"),
        "fee": transaction.get("fee"),
        "failed": transaction.get("failed"),
        "failed_reason": transaction.get("failed_reason"),
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    transaction_tag: Optional[str] = None,
    account_tag: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {
            "tenant": tenant,
            "transaction_tag": transaction_tag,
            "account_tag": account_tag,
        }
    result = await storage.db["transactions"].find_one(params)
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
                        "transaction_tag": re.compile(
                            re.escape(filter["q"]), re.IGNORECASE
                        )
                    },
                    {"account_tag": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    elif filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("transaction_tag"):
        filters_and.append({"transaction_tag": filter["transaction_tag"]})
    if filter.get("account_tag"):
        filters_and.append({"account_tag": filter["account_tag"]})
    if filter.get("invoice_number"):
        filters_and.append({"invoice_number": filter["invoice_number"]})
    if filter.get("primary") is not None:
        filters_and.append({"primary": bool(filter["primary"])})
    if filter.get("inbound") is not None:
        filters_and.append({"inbound": bool(filter["inbound"])})
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
    result = storage.db["transactions"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    transactions = [
        await serialize(storage, transaction)
        for transaction in await result.skip(page * perPage)
        .limit(perPage)
        .to_list(None)
    ]
    return transactions


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["transactions"].count_documents(query)
    return {"count": result}


async def upsert(storage: StorageService, transaction: dict) -> Optional[dict]:
    transaction = await process(storage, transaction)
    result = await storage.db["transactions"].find_one_and_update(
        {"_id": transaction.get("id")}
        if transaction.get("id")
        else {
            "tenant": transaction.get("tenant"),
            "transaction_tag": transaction.get("transaction_tag"),
            "account_tag": transaction.get("account_tag"),
        },
        {
            "$setOnInsert": {"_id": transaction.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": transaction.get("tenant"),
                    "transaction_tag": transaction.get("transaction_tag"),
                    "account_tag": transaction.get("account_tag"),
                    "source": transaction.get("source"),
                    "source_ip": transaction.get("source_ip"),
                    "carrier_ip": transaction.get("carrier_ip"),
                    "destination": transaction.get("destination"),
                    "primary": bool(transaction.get("primary")),
                    "inbound": bool(transaction.get("inbound")),
                    "tags": transaction.get("tags"),
                    "authorized": transaction.get("authorized"),
                    "destination_rate": transaction.get("destination_rate"),
                    "timestamp_auth": transaction.get("timestamp_auth"),
                    "timestamp_begin": transaction.get("timestamp_begin"),
                    "timestamp_end": transaction.get("timestamp_end"),
                    "duration": transaction.get("duration"),
                    "fee": transaction.get("fee"),
                    "failed": transaction.get("failed"),
                    "failed_reason": transaction.get("failed_reason"),
                }
            ),
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return await serialize(storage, result)


async def delete(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    transaction_tag: Optional[str] = None,
    account_tag: Optional[str] = None,
) -> Optional[dict]:
    transaction = await get(
        storage,
        id=id,
        tenant=tenant,
        transaction_tag=transaction_tag,
        account_tag=account_tag,
        role="W",
    )
    if transaction is not None:
        await storage.db["transactions"].delete_one({"_id": transaction["id"]})
    return transaction
