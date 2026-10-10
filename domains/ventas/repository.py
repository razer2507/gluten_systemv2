import os
from abc import ABC, abstractmethod
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv  # noqa: F401, RUF100
from psycopg.rows import dict_row

load_dotenv()


from domains.ventas.models import Venta


class VentasRepository(ABC):
    @abstractmethod
    def _get_conn(self):
        pass

    @abstractmethod
    def insert(self, venta: Venta) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id) -> Venta:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list:
        pass

    @abstractmethod
    def delete(self, venta: Venta) -> None:
        pass

    @abstractmethod
    def update(self, venta: Venta) -> None:
        pass


class PostgresVentasRepository(VentasRepository):
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

    def insert(self, venta: Venta) -> int:
        query_ventas = """
                INSERT INTO ventas(fecha,cliente_id,total,estado) VALUES(%(fecha)s,%(cliente_id)s,%(total)s,%(estado)s)
                RETURNING id
                """
        query_detalle_ventas = """
                INSERT INTO detalle_ventas(venta_id,producto_id,cantidad,precio_unitario) 
                VALUES (%(venta_id)s,%(producto_id)s,%(cantidad)s,%(precio_unitario)s);
                """
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query_ventas, venta.to_dict(exclude_id=True))
            venta_insertada_id = cursor.fetchone()["id"]
            productos = [
                producto.to_dict(venta_padre_id=venta_insertada_id)
                for producto in venta.productos
            ]
            cursor.executemany(query_detalle_ventas, productos)
            return venta_insertada_id

    def get_all(self) -> list:
        with self._get_conn() as conn, conn.cursor() as cursor:
            query = """ 
                SELECT 
                    v.id, v.fecha, v.cliente_id, v.total, v.estado,
                    COALESCE(json_agg(
                        json_build_object(
                            'id', b.id,
                            'venta_id', b.venta_id,
                            'producto_id', b.producto_id,
                            'cantidad', b.cantidad,
                            'precio_unitario', b.precio_unitario
                        )
                    ) FILTER (WHERE b.id IS NOT NULL), '[]') AS productos
                FROM ventas AS v
                LEFT JOIN detalle_ventas AS b ON v.id = b.venta_id
                GROUP BY v.id;
            """
            cursor.execute(query)
            items = cursor.fetchall()
            return [Venta.from_dict(data) for data in items]

    def get_by_id(self, id) -> Venta:
        query = """ 
                SELECT 
                    v.id, v.fecha, v.cliente_id, v.total, v.estado,
                    COALESCE(json_agg(
                        json_build_object(
                            'id', b.id,
                            'venta_id', b.venta_id,
                            'producto_id', b.producto_id,
                            'cantidad', b.cantidad,
                            'precio_unitario', b.precio_unitario
                        )
                    ) FILTER (WHERE b.id IS NOT NULL), '[]') AS productos
                FROM ventas AS v
                LEFT JOIN detalle_ventas AS b ON v.id = b.venta_id
                WHERE v.id = %(id)s
                GROUP BY v.id;
                """
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query, {"id": id})
            data = cursor.fetchone()
            return Venta.from_dict(data)

    def get_filtered(self, **kwargs) -> list:
        if not kwargs:
            raise psycopg.OperationalError
        query_base = """SELECT 
                            ventas.id,ventas.fecha,ventas.cliente_id,ventas.total,ventas.estado,COALESCE(
                            json_agg(
                            json_build_object(
                            'id',detalle_ventas.id,
                            'venta_id',detalle_ventas.venta_id,
                            'producto_id',detalle_ventas.producto_id,
                            'cantidad',detalle_ventas.cantidad,
                            'precio_unitario',detalle_ventas.precio_unitario
                            )
                            )FILTER(WHERE detalle_ventas.id IS NOT NULL),'[]') AS productos
                            FROM ventas
                            LEFT JOIN detalle_ventas ON ventas.id = detalle_ventas.venta_id
                            WHERE 1=1
                            """
        params = {}
        if kwargs.get("fecha_inicio") and kwargs.get("fecha_fin"):
            query_base += " AND ventas.fecha BETWEEN %(fecha_inicio)s AND %(fecha_fin)s"
            params["fecha_inicio"] = kwargs["fecha_inicio"]
            params["fecha_fin"] = kwargs["fecha_fin"]
        if kwargs.get("id_cliente"):
            query_base += " AND ventas.cliente_id = %(id_cliente)s"
            params["id_cliente"] = kwargs["id_cliente"]
        if kwargs.get("estado"):
            query_base += " AND ventas.estado = %(estado)s"
            params["estado"] = kwargs["estado"]
        if kwargs.get("total_min") and kwargs.get("total_max"):
            query_base += " AND ventas.total BETWEEN %(total_min)s AND %(total_max)s"
            params["total_min"] = kwargs["total_min"]
            params["total_max"] = kwargs["total_max"]
        elif kwargs.get("total_max"):
            query_base += " AND ventas.total >= %(total_max)s"
            params["total_max"] = kwargs["total_max"]

        query_base += " GROUP BY ventas.id ORDER BY ventas.fecha DESC;"
        with self._get_conn() as conn, conn.cursor() as cursor:
            cursor.execute(query_base, params)
            return [Venta.from_dict(data) for data in cursor.fetchall()]

    def update(self, venta: Venta) -> None:
        with self._get_conn() as conn, conn.cursor() as cursor:
            query = "UPDATE ventas SET fecha=%(fecha)s,cliente_id=%(cliente_id)s,total=%(total)s,estado=%(estado)s WHERE id=%(id)s"
            cursor.execute(query, venta.to_dict(exclude_id=False))

    def delete(self, venta: Venta) -> None:
        with self._get_conn() as conn, conn.cursor() as cursor:
            query = "DELETE FROM ventas WHERE id=%(id)s"
            cursor.execute(query, {"id": venta.id})

