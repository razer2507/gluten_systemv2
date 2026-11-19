# config/settings.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()  # una sola vez en todo el proyecto

@dataclass(frozen=True)
class DatabaseSettings():
    host: str | None = None
    port: int | None = None 
    dbname: str | None = None 
    user: str | None = None
    password: str | None = None
    conninfo : str | None = None

    @classmethod
    def test_from_env(cls) -> "DatabaseSettings":
            return cls(
            host=os.getenv("TEST_HOST", ""),
            port=int(os.getenv("TEST_PORT", "5432")),
            dbname=os.getenv("TEST_DATABASE", ""),
            user=os.getenv("TEST_USER", ""),
            password=os.getenv("TEST_PASSWORD", "")
            )
    @classmethod
    def from_env(cls)->'DatabaseSettings':
        return cls(
            conninfo=os.getenv('URL')
        )
