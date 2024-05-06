from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

from src.middleware.http_error_handling_middleware import ExceptionHandlerMiddleware
from src.services.auth.auth_router import oauth_router
from src.services.checks.check_router import check_router
from src.utils.logging.set_logging import set_logger
from src.settings.checkbox_settings import settings

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


from redis import asyncio as aioredis

logger = set_logger()

app = FastAPI(
    root_path=settings.api_prefix,
    title="CheckBox",
    description="CheckBox API",
    docs_url="/",
    swagger_ui_oauth2_redirect_url="/oauth2-redirect",
)

app.include_router(oauth_router)
app.include_router(check_router)


@app.on_event("startup")
async def startup():
    redis_url = settings.get_redis_url()
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


origins = ["*"]

app.add_middleware(ExceptionHandlerMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
