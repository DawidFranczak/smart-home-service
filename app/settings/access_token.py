from pathlib import Path

from pydantic_settings import BaseSettings

from pydantic import model_validator


def read_from_file(path: str) -> str:
    return Path(path).read_text()


class AccessTokenPublicKey(BaseSettings):
    JWT_PUBLIC_KEY_PATH: str
    PUBLIC_KEY: str | None = None

    @model_validator(mode="after")
    def lazy_load_public_key(self) -> "AccessTokenPublicKey":
        if not self.PUBLIC_KEY and self.JWT_PUBLIC_KEY_PATH:
            self.PUBLIC_KEY = read_from_file(self.JWT_PUBLIC_KEY_PATH)
        return self
