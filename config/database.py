# config/database.py
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
def transaction(settings:DatabaseSettings)-> psycopg.Connection:
    conn = get_conn(settings)
    try:
        yield conn
        conn.commit()

    except psycopg.OperationalError:
        conn.rollback()
        raise

    finally:
        conn.close()

#prueba rapida 

if __name__ == '__main__':
    with transaction(settings=DatabaseSettings.test_from_env()) as t:
        cursor = t.cursor()
        cursor.execute('SELECT * FROM ventas')
        print(cursor.fetchall())