import asyncio
import os
import pytest

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "rating_api_tests")


def run_synchronously(coroutine):
    event_loop = None
    try:
        event_loop = asyncio.get_event_loop()
    except RuntimeError:
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)
    return event_loop.run_until_complete(coroutine)


def _app(config):
    from rating_api.app import get_app

    app_obj = get_app(config)
    #
    from pymongo import MongoClient

    mongoclient = MongoClient(MONGODB_URI)
    mongoclient.drop_database(MONGODB_DB)
    # create the indexes
    storage_service = getattr(app_obj, 'storage_service')
    run_synchronously(storage_service.connect())
    run_synchronously(storage_service.create_indexes())
    run_synchronously(storage_service.close())
    # db is directly used in tests
    db = mongoclient[MONGODB_DB]
    setattr(app_obj, "db", db)
    # return the fixture
    return app_obj


@pytest.fixture(scope="function")
def app():
    config = dict(mongodb_uri=MONGODB_URI, mongodb_db=MONGODB_DB, debug=True)
    return _app(config)


@pytest.fixture(scope="function")
def client(app):
    from starlette.testclient import TestClient

    cli = TestClient(app)
    with cli:
        return cli
