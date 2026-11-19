from config.settings import DatabaseSettings
from domains.clientes.infrastructure.postgres_repo import (
    PostgresClientesRepository,
)
from domains.clientes.ports.repository import ClientesRepository
from domains.gastos.infrastructure.postgres_repo import PostgresGastosRepository
from domains.gastos.ports.repository import GastosRepository
from domains.productos.infrastructure.postgres_repo import (
    PostgresProductosRepository,
)
from domains.productos.ports.repository import ProductosRepository
from domains.ventas.app_services.service import RegistrarVentaUseCase
from domains.ventas.infrastructure.postgres_repo import PostgresVentasRepository
from domains.ventas.ports.repository import VentasRepository


class AppContext:
    def __init__(self, settings: DatabaseSettings):
        self.settings_db = settings
        self.venta_repo: VentasRepository = PostgresVentasRepository(
            self.settings_db
        )
        self.cliente_repo: ClientesRepository = PostgresClientesRepository(
            self.settings_db
        )
        self.producto_repo: ProductosRepository = PostgresProductosRepository(
            self.settings_db
        )
        self.gasto_repo: GastosRepository = PostgresGastosRepository(
            self.settings_db
        )
        self.registrar_venta = RegistrarVentaUseCase(
            ventas_repo=self.venta_repo,
            clientes_repo=self.cliente_repo,
        )
