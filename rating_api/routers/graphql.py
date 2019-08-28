import graphene  # type: ignore

from graphql.execution.executors.asyncio import AsyncioExecutor  # type: ignore
from fastapi import APIRouter
from starlette.graphql import GraphQLApp

from ..schema import Query, Mutations


router = APIRouter()

router.add_route(
    "/graphql",
    GraphQLApp(
        schema=graphene.Schema(query=Query, mutation=Mutations, auto_camelcase=False),
        executor_class=AsyncioExecutor,
    ),
)
