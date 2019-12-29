from graphql.execution.executors.asyncio import AsyncioExecutor  # type: ignore
from fastapi import APIRouter
from starlette.graphql import GraphQLApp

from ..graphql import schema


router = APIRouter()

router.add_route("/graphql", GraphQLApp(schema=schema, executor_class=AsyncioExecutor))
