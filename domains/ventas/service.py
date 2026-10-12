# domains/ventas/service.py
from datetime import date

from domains.clientes.repository import ClientesRepository
from domains.ventas.models import DetalleVenta, Venta
from domains.ventas.repository import VentasRepository
from domains.ventas.strategies import CanalVentaStrategy
from shared.exceptions import ClienteInvalidoError


class VentasService:
    """Servicio de aplicación para el dominio de ventas."""

    def __init__(
        self, venta_repo: VentasRepository, clientes_repo: ClientesRepository
    ) -> None:
        """Inyecta de forma única el contrato del repositorio de ventas."""
        self._venta_repo = venta_repo
        self._clientes_repo = clientes_repo

    def registrar_venta(
        self,
        cliente_id: int,
        productos: list[dict],
        canal: CanalVentaStrategy,
        fecha: date | str,
        estado: str = "en deuda",
    ) -> Venta:
        """Orquesta la creación de una venta delegando el cálculo a la estrategia del canal.
        Args:
            cliente_id: ID del cliente asociado a la venta.
            productos: Lista de ítems [{'producto_id': int, 'cantidad': int, 'precio_unitario': float}]
            canal: Instancia concreta del canal (estrategia OCP).
            fecha: Fecha de la transacción (opcional).
        """
        detalle_venta = [DetalleVenta.from_dict(data) for data in productos]
        subtotal = sum(item.subtotal_item for item in detalle_venta)
        total_calculado = self._resolver_estrategia(subtotal=subtotal, strategy=canal)
        nueva_venta = Venta(
            fecha=fecha,
            cliente_id=cliente_id,
            total=total_calculado,
            estado=estado,
            productos=detalle_venta,
        )

        #Persistir en la base de datos
        return self._venta_repo.insert(nueva_venta)

    def obtener_venta(self, venta_id: int) -> Venta | None:
        return self._venta_repo.get_by_id(venta_id)

    def listar_ventas(self) -> list[Venta]:
        return self._venta_repo.get_all()

    def _resolver_estrategia(self, subtotal: float, strategy: CanalVentaStrategy):
        return strategy.calcular_total(subtotal=subtotal)

    def _validar_cliente(self, cliente_id: int) -> None:
        if not self._clientes_repo.get_by_id(id):
            raise ClienteInvalidoError("El cliente seleccionado no es valido")