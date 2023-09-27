from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

import config
from api.system.views import api_system_router
from api.v1.views import api_v1_router
from middlewares import MIDDLEWARES

limiter = Limiter(key_func=get_remote_address, default_limits=[f"{config.MAX_LIMITER}/minute"])


def get_application() -> FastAPI:
    app_f = FastAPI(
        title=config.PROJECT_NAME,
        debug=config.DEBUG,
        version=config.VERSION,
    )

    app_f.include_router(api_system_router, prefix="/api/system")
    app_f.include_router(api_v1_router, prefix="/api/v1")

    if config.IS_LIMITER:
        app_f.state.limiter = limiter
        app_f.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app_f.add_middleware(SlowAPIMiddleware)

    for middleware in MIDDLEWARES:
        app_f.middleware("http")(middleware)

    return app_f


def application() -> FastAPI:
    app_f = get_application()

    @app_f.get("/")
    async def index():
        return RedirectResponse("/docs")

    return app_f


app: FastAPI = application()
