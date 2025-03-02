from pydantic_settings import BaseSettings, SettingsConfigDict


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class DBSettings(AppBaseSettings):
    model_config = SettingsConfigDict(env_prefix='DATABASE_')
    HOST: str
    PORT: str
    NAME: str
    USER: str
    PASSWORD: str


class AppSettings(AppBaseSettings):
    BACK_HOST: str
    BACK_PORT: int


settings = Settings()
