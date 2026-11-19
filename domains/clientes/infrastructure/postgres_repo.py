from config.database import transaction
from config.settings import DatabaseSettings
from domains.clientes.models import Cliente
from domains.clientes.ports.repository import ClientesRepository


class PostgresClientesRepository(ClientesRepository):
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings

    def insert(self, cliente: Cliente) -> int:
        query = """
                INSERT INTO clientes(nombre, referencia)
                VALUES (%(nombre)s, %(referencia)s)
                RETURNING id
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, cliente.to_dict(exclude_id=True))
            return cursor.fetchone()["id"]

    def get_all(self) -> list[Cliente]:
        query = "SELECT id, nombre, referencia FROM clientes ORDER BY nombre"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return [Cliente.from_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, id: int) -> Cliente | None:
        query = "SELECT id, nombre, referencia FROM clientes WHERE id = %(id)s"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": id})
            return Cliente.from_dict(cursor.fetchone())

    def get_filtered(self, **kwargs) -> list[Cliente]:
        query = "SELECT id, nombre, referencia FROM clientes WHERE 1=1"
        params = {}
        if kwargs.get("nombre"):
            query += " AND nombre ILIKE %(nombre)s"
            params["nombre"] = f"%{kwargs['nombre']}%"
        if kwargs.get("referencia"):
            query += " AND referencia = %(referencia)s"
            params["referencia"] = kwargs["referencia"]
        query += " ORDER BY nombre"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            return [Cliente.from_dict(row) for row in cursor.fetchall()]

    def update(self, cliente: Cliente) -> None:
        query = "UPDATE clientes SET nombre=%(nombre)s, referencia=%(referencia)s WHERE id=%(id)s"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, cliente.to_dict(exclude_id=False))

    def delete(self, cliente: Cliente) -> None:
        query = "DELETE FROM clientes WHERE id=%(id)s"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": cliente.id})
