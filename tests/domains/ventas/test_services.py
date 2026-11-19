from datetime import date

from config.settings import DatabaseSettings
from domains.clientes.infrastructure.postgres_repo import (
    PostgresClientesRepository,
)
from domains.ventas.app_services.service import RegistrarVentaUseCase
from domains.ventas.infrastructure.postgres_repo import (
    PostgresVentasRepository,
)

settings = DatabaseSettings.test_from_env()
repository_postgres = PostgresVentasRepository(settings)
clientes_repo = PostgresClientesRepository(settings)
service = RegistrarVentaUseCase(
    ventas_repo=repository_postgres,
    clientes_repo=clientes_repo,
)


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
