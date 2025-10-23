from pydantic_settings import BaseSettings


class AccessToken(BaseSettings):
    ACCESS_TOKEN: str
