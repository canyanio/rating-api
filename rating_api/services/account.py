import re

from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4
from pymongo import ASCENDING, DESCENDING  # type: ignore
from pymongo.collection import ReturnDocument  # type: ignore

from . import customer as customer_service
from .storage import StorageService


async def process(storage: StorageService, account: dict) -> dict:
    account = account.copy()
    #
    if account.get("customer_tag"):
        customer = await customer_service.get(
            storage,
            tenant=account.get("tenant"),
            customer_tag=account.get("customer_tag"),
        )
        if customer is None:
            raise ValueError(
                "Customer with tag = %s not found in tenant %s!"
                % (account.get("customer_tag"), account.get("tenant"))
            )
        account["customer_tag"] = customer["customer_tag"]
    return account


async def serialize(storage: StorageService, account: dict) -> dict:
    account = await process(storage, account)
    customer = (
        await customer_service.get(
            storage,
            tenant=account.get("tenant"),
            customer_tag=account.get("customer_tag"),
        )
        if account.get("customer_tag")
        else None
    )
    if account.get('linked_accounts') is not None:
        linked_accounts = await get_accounts(
            storage, account["tenant"], account["linked_accounts"]
        )
    else:
        linked_accounts = []
    return {
        "id": account.get("_id"),
        "tenant": account.get("tenant"),
        "account_tag": account.get("account_tag"),
        "name": account.get("name"),
        "type": account.get("type"),
        "customer_tag": customer["id"] if customer else None,
        "customer": customer,
        "balance": account.get("balance"),
        "notification_email": account.get("notification_email"),
        "notification_mobile": account.get("notification_mobile"),
        "active": bool(account.get("active"))
        if account.get("active") is not None
        else None,
        "max_concurrent_transactions": account.get("max_concurrent_transactions"),
        "max_inbound_transactions": account.get("max_inbound_transactions"),
        "max_outbound_transactions": account.get("max_outbound_transactions"),
        "running_transactions": account.get("running_transactions") or (),
        "carrier_tags": account.get("carrier_tags"),
        "carrier_tags_override": account.get("carrier_tags_override"),
        "pricelist_tags": account.get("pricelist_tags"),
        "tags": account.get("tags"),
        "linked_accounts": linked_accounts,
    }


async def get(
    storage: StorageService,
    id: Optional[str] = None,
    tenant: Optional[str] = None,
    account_tag: Optional[str] = None,
    role: str = "R",
) -> Optional[dict]:
    params: dict
    if id is not None:
        params = {"_id": id}
    else:
        params = {"tenant": tenant, "account_tag": account_tag}
    account = await storage.db["accounts"].find_one(params)
    return await serialize(storage, account) if account is not None else None


async def get_query(storage: StorageService, filter: Optional[dict] = None) -> dict:
    filter = filter or {}
    filters_and: List = []
    if filter.get("q"):
        filters_and.append(
            {
                "$or": [
                    {"tenant": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"account_tag": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                    {"name": re.compile(re.escape(filter["q"]), re.IGNORECASE)},
                ]
            }
        )
    if filter.get("id"):
        filters_and.append({"_id": filter["id"]})
    if filter.get("ids"):
        filters_and.append({"_id": {"$in": filter["ids"]}})
    if filter.get("tenant"):
        filters_and.append({"tenant": filter["tenant"]})
    if filter.get("account_tag"):
        filters_and.append({"account_tag": filter["account_tag"]})
    if filter.get("type"):
        filters_and.append({"type": filter["type"]})
    if filter.get("active"):
        filters_and.append({"active": filter["active"]})
    if filter.get("with_running_transactions"):
        filters_and.append(
            {
                "running_transactions": {
                    "$elemMatch": {"in_progress": True, "inbound": False}
                }
            }
        )
    if filter.get("with_long_running_transactions"):
        filters_and.append(
            {
                "running_transactions": {
                    "$elemMatch": {
                        "in_progress": True,
                        "timestamp_begin": {
                            "$lte": datetime.utcnow() - timedelta(seconds=3600 * 3)
                        },
                    }
                }
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
    result = storage.db["accounts"].find(query)
    result = result.sort(
        sortField if sortField != "id" else "_id",
        sortOrder.lower() == "asc" and ASCENDING or DESCENDING,
    )
    accounts = [
        await serialize(storage, account)
        for account in await result.skip(page * perPage).limit(perPage).to_list(None)
    ]
    return accounts


async def get_all_meta(
    storage: StorageService,
    page: int = 0,
    perPage: int = 25,
    sortField: str = "id",
    sortOrder: str = "asc",
    filter: Optional[dict] = None,
) -> dict:
    query = await get_query(storage, filter)
    result = await storage.db["accounts"].count_documents(query)
    return {"count": result}


async def get_accounts(
    storage: StorageService, tenant: str, account_tags: list
) -> List[dict]:
    if not account_tags:
        return []
    results = (
        await storage.db["accounts"]
        .find({"tenant": tenant, "account_tag": {"$in": account_tags}})
        .to_list(None)
    )
    return (
        [
            {
                "tenant": tenant,
                "account_tag": result.get("account_tag"),
                "name": result.get("name"),
                "type": result.get("type"),
                "balance": result.get("balance"),
                "notification_email": result.get("notification_email"),
                "notification_mobile": result.get("notification_mobile"),
                "active": bool(result.get("active"))
                if result.get("active") is not None
                else None,
                "max_concurrent_transactions": result.get(
                    "max_concurrent_transactions"
                ),
                "max_inbound_transactions": result.get("max_inbound_transactions"),
                "max_outbound_transactions": result.get("max_outbound_transactions"),
                "running_transactions": result.get("running_transactions") or (),
                "carrier_tags": result.get("carrier_tags"),
                "carrier_tags_override": result.get("carrier_tags_override"),
                "pricelist_tags": result.get("pricelist_tags"),
                "tags": result.get("tags"),
            }
            for result in results
        ]
        if results is not None
        else []
    )


async def get_transaction(
    storage: StorageService, tenant: str, account_tag: str, transaction_tag: str
) -> Optional[dict]:
    result = await storage.db["accounts"].find_one(
        {
            "tenant": tenant,
            "account_tag": account_tag,
            "running_transactions.transaction_tag": transaction_tag,
        },
        {"_id": 1, "running_transactions.$": 1},
    )
    transaction = result.get("running_transactions")[0] if result is not None else None
    return (
        {
            "destination_rate": transaction.get("destination_rate"),
            "transaction_tag": transaction.get("transaction_tag"),
            "proxy_tag": transaction.get("proxy_tag"),
            "source": transaction.get("source"),
            "source_ip": transaction.get("source_ip"),
            "destination": transaction.get("destination"),
            "carrier_ip": transaction.get("carrier_ip"),
            "tags": transaction.get("tags"),
            "in_progress": transaction.get("in_progress"),
            "inbound": transaction.get("inbound"),
            "primary": transaction.get("primary"),
            "timestamp_begin": transaction.get("timestamp_begin"),
            "timestamp_end": transaction.get("timestamp_end"),
        }
        if result is not None
        else None
    )


async def upsert(storage: StorageService, account: dict) -> Optional[dict]:
    account = await process(storage, account)
    result = await storage.db["accounts"].find_one_and_update(
        {"_id": account.get("id")}
        if account.get("id")
        else {
            "tenant": account.get("tenant"),
            "account_tag": account.get("account_tag"),
        },
        {
            "$setOnInsert": {"_id": account.get("id") or str(uuid4())},
            "$set": storage.filter_dict(
                {
                    "tenant": account.get("tenant"),
                    "account_tag": account.get("account_tag"),
                    "name": account.get("name"),
                    "type": account.get("type"),
                    "customer_tag": account.get("customer_tag"),
                    "notification_email": account.get("notification_email"),
                    "notification_mobile": account.get("notification_mobile"),
                    "active": bool(account.get("active"))
                    if account.get("active") is not None
                    else None,
                    "balance": account.get("balance"),
                    "max_concurrent_transactions": account.get(
                        "max_concurrent_transactions"
                    ),
                    "max_inbound_transactions": account.get("max_inbound_transactions"),
                    "max_outbound_transactions": account.get(
                        "max_outbound_transactions"
                    ),
                    "carrier_tags": account.get("carrier_tags"),
                    "carrier_tags_override": account.get("carrier_tags_override"),
                    "pricelist_tags": account.get("pricelist_tags"),
                    "tags": account.get("tags"),
                    "linked_accounts": account.get("linked_accounts"),
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
    account_tag: Optional[str] = None,
) -> Optional[dict]:
    account = await get(
        storage, id=id, tenant=tenant, account_tag=account_tag, role="W"
    )
    if account is not None:
        await storage.db["accounts"].delete_one({"_id": account["id"]})
    return account


async def set_balance(
    storage: StorageService,
    tenant: str,
    account_tag: str,
    tags: tuple,
    balance: int,
    operation: str = "$set",
) -> Optional[bool]:
    query: dict = {"tenant": tenant}
    if account_tag is not None:
        query["account_tag"] = account_tag
    if tags:
        query["tags"] = {"$in": tags}
    result = await storage.db["accounts"].update_many(
        query, {operation: {"balance": balance}}
    )
    return bool(result.matched_count)


async def increment_balance(
    storage: StorageService, tenant: str, account_tag: str, tags: tuple, balance: int
) -> Optional[bool]:
    return await set_balance(
        storage, tenant, account_tag, tags, balance, operation="$inc"
    )


async def begin_transaction(
    storage: StorageService, tenant: str, account_tag: str, transaction: dict
) -> Optional[dict]:
    result = await storage.db["accounts"].find_one_and_update(
        {"tenant": tenant, "account_tag": account_tag},
        {
            "$addToSet": {
                "running_transactions": {
                    "proxy_tag": transaction.get("proxy_tag"),
                    "destination_rate": transaction.get("destination_rate"),
                    "transaction_tag": transaction.get("transaction_tag"),
                    "source": transaction.get("source"),
                    "source_ip": transaction.get("source_ip"),
                    "destination": transaction.get("destination"),
                    "carrier_ip": transaction.get("carrier_ip"),
                    "tags": transaction.get("tags"),
                    "in_progress": True,
                    "inbound": bool(transaction.get("inbound")),
                    "primary": bool(transaction.get("primary")),
                    "timestamp_begin": transaction.get("timestamp_begin"),
                    "timestamp_end": None,
                }
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    result = (
        tuple(
            filter(
                lambda x: x["transaction_tag"] == x["transaction_tag"],
                result.get("running_transactions"),
            )
        )
        if result
        else None
    )
    if result is None:
        return None
    return result[0]


async def end_transaction(
    storage: StorageService,
    tenant: str,
    account_tag: str,
    transaction_tag: str,
    timestamp_end: datetime,
) -> Optional[dict]:
    result = await storage.db["accounts"].find_one_and_update(
        {
            "tenant": tenant,
            "account_tag": account_tag,
            "running_transactions.transaction_tag": transaction_tag,
        },
        {
            "$set": {
                "running_transactions.$.timestamp_end": timestamp_end,
                "running_transactions.$.in_progress": False,
            }
        },
        return_document=ReturnDocument.AFTER,
    )
    if result is None:
        return None
    return await get_transaction(storage, tenant, account_tag, transaction_tag)


async def commit_transaction(
    storage: StorageService,
    tenant: str,
    account_tag: str,
    transaction_tag: str,
    fee: int,
) -> Optional[bool]:
    result = await storage.db["accounts"].find_one_and_update(
        {
            "tenant": tenant,
            "account_tag": account_tag,
            "running_transactions.transaction_tag": transaction_tag,
        },
        {
            "$inc": {"balance": -fee},
            "$pull": {"running_transactions": {"transaction_tag": transaction_tag}},
        },
        return_document=ReturnDocument.AFTER,
    )
    if result:
        return True
    return False


async def rollback_transaction(
    storage: StorageService, tenant: str, account_tag: str, transaction_tag: str
) -> Optional[bool]:
    result = await storage.db["accounts"].find_one_and_update(
        {
            "tenant": tenant,
            "account_tag": account_tag,
            "running_transactions.transaction_tag": transaction_tag,
        },
        {"$pull": {"running_transactions": {"transaction_tag": transaction_tag}}},
        return_document=ReturnDocument.AFTER,
    )
    if result:
        return True
    return False
