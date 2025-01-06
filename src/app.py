from contextlib import asynccontextmanager
from os import environ

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.security import cors_settings
from src.utils.database import db_manager
from src.utils.rsa_keys_manager import keys_manager


@asynccontextmanager
async def _lifespan(app_: FastAPI):  # noqa: ANN202, ARG001
    keys_manager.generate_keys()
    async with db_manager.lifespan():
        yield


app = FastAPI(
    lifespan=_lifespan,
    title='Movie RecSys backend',
)

# app.include_router(
#     auth_router,
#     prefix='/auth',
#     tags=['auth'],
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_settings.origins,
    allow_credentials=cors_settings.credentials,
    allow_methods=cors_settings.methods,
    allow_headers=cors_settings.headers,
)

environ['TZ'] = 'Europe/Saratov'
