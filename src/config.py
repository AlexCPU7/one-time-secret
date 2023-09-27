import os

from starlette.config import Config

if os.path.exists("env"):
    config = Config("./deploy/local/.env.local")
else:
    config = Config()

PROJECT_NAME: str = config("PROJECT_NAME", cast=str)
VERSION: str = config("VERSION", cast=str)
DEBUG: bool = config("VERSION", default=True)

IS_LIMITER: bool = config("IS_LIMITER", default=True)
MAX_LIMITER: int = config("MAX_LIMITER", cast=int, default=600)

KEY_HASH: bytes = config("KEY_HASH", cast=str).encode('utf-8')

PORT_EXTERNAL: int = config("PORT_EXTERNAL", cast=int)

DB_HOST: str = config("DB_HOST", cast=str)
DB_NAME: str = config("DB_NAME", cast=str)
DB_USER: str = config("DB_USER", cast=str)
DB_PASSWORD: str = config("DB_PASSWORD", cast=str)
DB_PORT_EXTERNAL: int = config("DB_PORT_EXTERNAL", cast=int)

DB_DSN = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT_EXTERNAL}/{DB_NAME}"
