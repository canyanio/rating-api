from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase  # type: ignore
from pymongo import ASCENDING  # type: ignore

from fastapi import FastAPI
from starlette.requests import Request


class StorageService(object):

    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase

    def __init__(self, mongodb_uri: str, mongodb_db: str):
        self._mongodb_uri = mongodb_uri
        self._mongodb_db = mongodb_db

    async def connect(self):
        self.client = AsyncIOMotorClient(self._mongodb_uri)
        self.db = self.client[self._mongodb_db]

    async def create_indexes(self):
        await self.db["users"].create_index([("email", ASCENDING)], unique=True)
        await self.db["tenants"].create_index([("tenant", ASCENDING)], unique=True)
        await self.db["carriers"].create_index(
            [("tenant", ASCENDING), ("carrier_tag", ASCENDING)], unique=True
        )
        await self.db["customers"].create_index(
            [("tenant", ASCENDING), ("customer_tag", ASCENDING)], unique=True
        )
        await self.db["sellers"].create_index(
            [("tenant", ASCENDING), ("seller_tag", ASCENDING)], unique=True
        )
        await self.db["invoices"].create_index(
            [("tenant", ASCENDING), ("invoice_number", ASCENDING)], unique=True
        )
        await self.db["pricelists"].create_index(
            [("tenant", ASCENDING), ("pricelist_tag", ASCENDING)], unique=True
        )
        await self.db["pricelist_rates"].create_index(
            [
                ("tenant", ASCENDING),
                ("pricelist_tag", ASCENDING),
                ("prefix", ASCENDING),
                ("carrier_tag", ASCENDING),
            ],
            unique=True,
        )
        await self.db["pricelist_rates"].create_index(
            [("tenant", ASCENDING), ("prefix", ASCENDING), ("pricelist_tag", ASCENDING)]
        )
        await self.db["accounts"].create_index(
            [("tenant", ASCENDING), ("account_tag", ASCENDING)], unique=True
        )
        await self.db["accounts"].create_index(
            [
                ("tenant", ASCENDING),
                ("account_tag", ASCENDING),
                ("running_transactions.transaction_tag", ASCENDING),
            ]
        )
        await self.db["accounts"].create_index(
            [
                ("tenant", ASCENDING),
                ("type", ASCENDING),
                ("running_transactions.in_progress", ASCENDING),
            ]
        )
        await self.db["transactions"].create_index(
            [
                ("tenant", ASCENDING),
                ("transaction_tag", ASCENDING),
                ("account_tag", ASCENDING),
            ],
            unique=True,
        )

    async def connect_and_create_indexes(self):
        await self.connect()
        await self.create_indexes()

    async def close(self):
        self.client.close()

    def filter_dict(self, d: dict) -> dict:
        return dict([(k, v) for k, v in d.items() if v is not None])


def get(request: Request) -> StorageService:
    return request.state.storage


def setup(app: FastAPI, config: dict) -> FastAPI:
    storage_service = StorageService(
        mongodb_uri=config["mongodb_uri"], mongodb_db=config["mongodb_db"]
    )
    setattr(app, "storage_service", storage_service)

    app.add_event_handler("startup", storage_service.connect_and_create_indexes)
    app.add_event_handler("shutdown", storage_service.close)

    @app.middleware("http")
    async def storage_middleware(request: Request, call_next):
        request.state.storage = storage_service
        response = await call_next(request)
        return response

    _ = storage_middleware

    return app
