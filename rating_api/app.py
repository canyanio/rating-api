from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routers import graphql
from .routers import status
from .services import storage as storage_service


def get_app(config: dict):
    app = FastAPI()
    setattr(app, 'config', config)

    app.include_router(graphql.router)
    app.include_router(status.router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app = storage_service.setup(app, config)

    return app
