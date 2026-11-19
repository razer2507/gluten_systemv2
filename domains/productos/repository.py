from abc import ABC, abstractmethod

from config.database import transaction
from config.settings import DatabaseSettings
from domains.productos.models import Producto


class ProductosRepository(ABC):
    @abstractmethod
    def insert(self, producto: Producto) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Producto | None:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Producto]:
        pass

    @abstractmethod
    def update(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def delete(self, producto: Producto) -> None:
        pass


class PostgresProductosRepository(ProductosRepository):
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings

    def insert(self, producto: Producto) -> int:
        query = """
                INSERT INTO productos(nombre, precio_costo, categoria)
                VALUES (%(nombre)s, %(precio_costo)s, %(categoria)s)
                RETURNING id
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, producto.to_dict(exclude_id=True))
            return cursor.fetchone()["id"]

    def get_all(self) -> list[Producto]:
        query = """
                SELECT id, nombre, precio_costo, categoria
                FROM productos
                ORDER BY nombre
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return [Producto.from_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, id: int) -> Producto | None:
        query = """
                SELECT id, nombre, precio_costo, categoria
                FROM productos
                WHERE id = %(id)s
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": id})
            return Producto.from_dict(cursor.fetchone())

    def get_filtered(self, **kwargs) -> list[Producto]:
        query = """
                SELECT id, nombre, precio_costo, categoria
                FROM productos
                WHERE 1=1
                """
        params = {}
        if kwargs.get("nombre"):
            query += " AND nombre ILIKE %(nombre)s"
            params["nombre"] = f"%{kwargs['nombre']}%"
        if kwargs.get("categoria"):
            query += " AND categoria = %(categoria)s"
            params["categoria"] = kwargs["categoria"]
        if kwargs.get("precio_min") is not None:
            query += " AND precio_costo >= %(precio_min)s"
            params["precio_min"] = kwargs["precio_min"]
        if kwargs.get("precio_max") is not None:
            query += " AND precio_costo <= %(precio_max)s"
            params["precio_max"] = kwargs["precio_max"]
        query += " ORDER BY nombre"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            return [Producto.from_dict(row) for row in cursor.fetchall()]

    def update(self, producto: Producto) -> None:
        query = """
                UPDATE productos
                SET nombre = %(nombre)s,
                    precio_costo = %(precio_costo)s,
                    categoria = %(categoria)s
                WHERE id = %(id)s
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, producto.to_dict(exclude_id=False))

    def delete(self, producto: Producto) -> None:
        query = "DELETE FROM productos WHERE id = %(id)s"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": producto.id})
