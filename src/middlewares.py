from fastapi import Request
from loguru import logger
from starlette.responses import JSONResponse


async def exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.opt(exception=exc).error(f"Error - {exc.__class__.__name__}: {exc}")
        return JSONResponse(
            content="An internal error has occurred, please contact the server administrator",
            status_code=400
        )

MIDDLEWARES = (
    exceptions_middleware,
)
