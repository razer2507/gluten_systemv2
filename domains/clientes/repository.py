import os
from abc import ABC, abstractmethod
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv  # noqa: F401, RUF100
from psycopg.rows import dict_row

from domains.clientes.models import Cliente

load_dotenv()


class ClientesRepository(ABC):
    @abstractmethod
    def _get_conn(self):
        pass

    @abstractmethod
    def insert(self, cliente: Cliente) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Cliente]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Cliente:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Cliente]:
        pass

    @abstractmethod
    def delete(self, cliente: Cliente) -> None:
        pass

    @abstractmethod
    def update(self, cliente: Cliente) -> None:
        pass


class PostgresClientesRepository(ClientesRepository):
    @contextmanager
    def _get_conn(self):
        conn = psycopg.connect(
            host=os.getenv("TEST_HOST"),
            dbname=os.getenv("TEST_DATABASE"),
            user=os.getenv("TEST_USER"),
            password=os.getenv("TEST_PASSWORD"),
            port=os.getenv("TEST_PORT"),
            row_factory=dict_row,
        )
        try:
            yield conn
            conn.commit()
        except psycopg.Error as e:
            conn.rollback()
            print(e)
        finally:
            conn.close()

    def insert(self, cliente: Cliente) -> int:
        query = """
                INSERT INTO clientes(nombre, referencia) 
                VALUES (%(nombre)s, %(referencia)s)
                RETURNING id
                """
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, cliente.to_dict(exclude_id=True))
            return cursor.fetchone()["id"]

    def get_all(self) -> list[Cliente]:
        query = "SELECT id, nombre, referencia FROM clientes"
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query)
            items = cursor.fetchall()
            return [Cliente.from_dict(data) for data in items]

    def get_by_id(self, id: int) -> Cliente:
        query = "SELECT id, nombre, referencia FROM clientes WHERE id = %(id)s"
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": id})
            data = cursor.fetchone()
            return Cliente.from_dict(data)

    def get_filtered(self, **kwargs) -> list[Cliente]:
        # Based on a simple filtering pattern
        query = "SELECT id, nombre, referencia FROM clientes WHERE 1=1"
        params = {}
        if kwargs.get("nombre"):
            query += " AND nombre = %(nombre)s"
            params["nombre"] = kwargs["nombre"]
        if kwargs.get("referencia"):
            query += " AND referencia = %(referencia)s"
            params["referencia"] = kwargs["referencia"]
            
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            return [Cliente.from_dict(data) for data in cursor.fetchall()]

    def update(self, cliente: Cliente) -> None:
        query = "UPDATE clientes SET nombre=%(nombre)s, referencia=%(referencia)s WHERE id=%(id)s"
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, cliente.to_dict(exclude_id=False))

    def delete(self, cliente: Cliente) -> None:
        query = "DELETE FROM clientes WHERE id=%(id)s"
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": cliente.id})
