from config.database import transaction
from config.settings import DatabaseSettings
from domains.gastos.models import Gasto
from domains.gastos.ports.repository import GastosRepository


class PostgresGastosRepository(GastosRepository):
    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings

    def insert(self, gasto: Gasto) -> int:
        query = """
                INSERT INTO gastos(fecha, categoria, monto, descripcion, tipo)
                VALUES (%(fecha)s, %(categoria)s, %(monto)s, %(descripcion)s, %(tipo)s)
                RETURNING id
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, gasto.to_dict(exclude_id=True))
            return cursor.fetchone()["id"]

    def get_all(self) -> list[Gasto]:
        query = """
                SELECT id, fecha, categoria, monto, descripcion, tipo
                FROM gastos
                ORDER BY fecha DESC
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query)
            return [Gasto.from_dict(row) for row in cursor.fetchall()]

    def get_by_id(self, id: int) -> Gasto | None:
        query = """
                SELECT id, fecha, categoria, monto, descripcion, tipo
                FROM gastos
                WHERE id = %(id)s
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": id})
            return Gasto.from_dict(cursor.fetchone())

    def get_filtered(self, **kwargs) -> list[Gasto]:
        query = """
                SELECT id, fecha, categoria, monto, descripcion, tipo
                FROM gastos
                WHERE 1=1
                """
        params = {}
        if kwargs.get("fecha_inicio") and kwargs.get("fecha_fin"):
            query += " AND fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s"
            params["fecha_inicio"] = kwargs["fecha_inicio"]
            params["fecha_fin"] = kwargs["fecha_fin"]
        elif kwargs.get("fecha_inicio"):
            query += " AND fecha >= %(fecha_inicio)s"
            params["fecha_inicio"] = kwargs["fecha_inicio"]
        elif kwargs.get("fecha_fin"):
            query += " AND fecha <= %(fecha_fin)s"
            params["fecha_fin"] = kwargs["fecha_fin"]
        if kwargs.get("categoria"):
            query += " AND categoria = %(categoria)s"
            params["categoria"] = kwargs["categoria"]
        if kwargs.get("tipo"):
            query += " AND tipo = %(tipo)s"
            params["tipo"] = kwargs["tipo"]
        if kwargs.get("monto_min") is not None:
            query += " AND monto >= %(monto_min)s"
            params["monto_min"] = kwargs["monto_min"]
        if kwargs.get("monto_max") is not None:
            query += " AND monto <= %(monto_max)s"
            params["monto_max"] = kwargs["monto_max"]
        query += " ORDER BY fecha DESC"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, params)
            return [Gasto.from_dict(row) for row in cursor.fetchall()]

    def update(self, gasto: Gasto) -> None:
        query = """
                UPDATE gastos
                SET fecha = %(fecha)s,
                    categoria = %(categoria)s,
                    monto = %(monto)s,
                    descripcion = %(descripcion)s,
                    tipo = %(tipo)s
                WHERE id = %(id)s
                """
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, gasto.to_dict(exclude_id=False))

    def delete(self, gasto: Gasto) -> None:
        query = "DELETE FROM gastos WHERE id = %(id)s"
        with transaction(self._settings) as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": gasto.id})
