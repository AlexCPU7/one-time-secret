from fastapi import HTTPException, APIRouter

api_system_router = APIRouter()


@api_system_router.get("/ping", tags=["system"])
async def ping_pong():
    raise HTTPException(status_code=404, detail="Pong")


@api_system_router.get("/status_server", tags=["system"])
async def status_server():
    return {"data": "OK"}
