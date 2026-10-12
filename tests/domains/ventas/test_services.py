from datetime import date

from domains.clientes.repository import ClientesRepository
from domains.ventas.repository import (  # noqa: F401
    PostgresVentasRepository,
    VentasRepository,
)
from domains.ventas.service import VentasService
from domains.ventas.strategies import (
    CanalPedidosYaStrategy,  # noqa: F401, RUF100
    CanalPresencialStrategy,  # noqa: F401
    CanalVentaStrategy,  # noqa: F401
)

repository_postgres = PostgresVentasRepository()
service = VentasService(
    venta_repo=repository_postgres,
    clientes_repo=ClientesRepository
)

def test_registrar_venta():
    # la ui devuelve como que una vaina asi
    venta_valida = {
        "cliente_id": 1,
        "fecha": date.today(),
        'canal':CanalPedidosYaStrategy(),  
        "productos":[
            {
            'producto_id':1,
            'cantidad':2,
            'precio_unitario':2.5
            },
            {
            'producto_id':2,
            'cantidad':3,
            'precio_unitario':5.0
            }
            ]
    }
    id_venta_valida = service.registrar_venta(**venta_valida)
    assert(bool(repository_postgres.get_by_id(id_venta_valida)))