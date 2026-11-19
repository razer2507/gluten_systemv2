from datetime import date

from config.settings import DatabaseSettings
from domains.ventas.repository import PostgresVentasRepository
from domains.ventas.service import VentasService

repository_postgres = PostgresVentasRepository(DatabaseSettings.test_from_env())
service = VentasService(venta_repo=repository_postgres)


def test_registrar_venta():
    venta_valida = {
        "cliente_id": 1,
        "fecha": date.today(),
        "canal": "presencial",
        "productos": [
            {
                "producto_id": 1,
                "cantidad": 2,
                "precio_unitario": 2.5,
            },
            {
                "producto_id": 2,
                "cantidad": 3,
                "precio_unitario": 5.0,
            },
        ],
    }
    id_venta_valida = service.registrar_venta(**venta_valida)
    assert bool(repository_postgres.get_by_id(id_venta_valida))
