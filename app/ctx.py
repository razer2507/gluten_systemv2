from domains.ventas.repository import PostgresVentasRepository, VentasRepository
from domains.ventas.service import VentasService
from domains.ventas.ui.view import VentasView
from config.settings import DatabaseSettings


class AppContext:
    def __init__(self, settings: DatabaseSettings):
        self.settings_db = settings
        self.venta_repo: VentasRepository = PostgresVentasRepository(self.settings_db)
        self.venta_service: VentasService = VentasService(venta_repo=self.venta_repo)
