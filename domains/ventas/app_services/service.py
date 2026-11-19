from datetime import date

from domains.clientes.ports.repository import ClientesRepository
from domains.ventas.domain_services.strategies import CanalFactory, CanalVentaStrategy
from domains.ventas.models import DetalleVenta, Venta
from domains.ventas.ports.repository import VentasRepository
from shared.exceptions import ClienteInvalidoError


class RegistrarVentaUseCase:
    def __init__(
        self,
        ventas_repo: VentasRepository,
        clientes_repo: ClientesRepository,
        canal_factory: CanalFactory | None = None,
    ) -> None:
        self._ventas_repo = ventas_repo
        self._clientes_repo = clientes_repo
        self._canal_factory = canal_factory or CanalFactory()

    def registrar_venta(
        self,
        cliente_id: int,
        productos: list[dict],
        canal: str,
        fecha: date | str,
        estado: str = "en deuda",
    ) -> int:
        if self._clientes_repo.get_by_id(cliente_id) is None:
            raise ClienteInvalidoError("El cliente seleccionado no existe")

        detalle_venta = [DetalleVenta.from_dict(data) for data in productos]
        subtotal = sum(item.subtotal_item for item in detalle_venta)
        estrategia = self._canal_factory.obtener_canal(canal_nombre=canal)
        total_calculado = self._resolver_estrategia(
            subtotal=subtotal,
            strategy=estrategia,
        )
        nueva_venta = Venta(
            fecha=fecha,
            cliente_id=cliente_id,
            total=total_calculado,
            estado=estado,
            productos=detalle_venta,
        )

        return self._ventas_repo.insert(nueva_venta)

    def _resolver_estrategia(
        self, subtotal: float, strategy: CanalVentaStrategy
    ) -> float:
        return strategy.calcular_total(subtotal=subtotal)
