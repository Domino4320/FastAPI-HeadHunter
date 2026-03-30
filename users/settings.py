from pydantic_settings import BaseSettings, SettingsConfigDict


class CryptSettings(BaseSettings):
    ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(env_file=".env")


crypt_settings = CryptSettings()
