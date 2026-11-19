# config/database.py
from collections.abc import Iterator
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from config.settings import DatabaseSettings


def get_conn(settings:DatabaseSettings) -> psycopg.Connection:
    return psycopg.connect(
        row_factory=dict_row,
        **{k:v for k,v in vars(settings).items() if v is not None}
    )

@contextmanager
def transaction(settings: DatabaseSettings) -> Iterator[psycopg.Connection]:
    conn = get_conn(settings)
    try:
        yield conn
        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

