from os import getenv

from pydantic_settings import BaseSettings


class _CORSSettings(BaseSettings):
    origins: list[str] = getenv('CORS_ORIGINS').split('|')
    credentials: bool = True
    methods: list[str] = ['*']
    headers: list[str] = ['*']


cors_settings = _CORSSettings()
