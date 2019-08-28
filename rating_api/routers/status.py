from fastapi import APIRouter

from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT


router = APIRouter()


@router.get("/status")
async def status():
    return Response(status_code=HTTP_204_NO_CONTENT)
