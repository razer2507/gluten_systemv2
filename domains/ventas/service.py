# domains/ventas/service.py
from datetime import date

from domains.clientes.repository import ClientesRepository
from domains.ventas.models import DetalleVenta, Venta
from domains.ventas.repository import VentasRepository
from domains.ventas.strategies import CanalVentaStrategy
from shared.exceptions import (
    ClienteInvalidoError,
    EstadoInvalidoError,
    FechaInvalidaError,
    TotalInvalidoError,
    VentaSinProductosError,
)


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
        items: list[dict],
        canal: CanalVentaStrategy,
        fecha: date or str,
        estado : str = 'en deuda'
    ) -> Venta:
        """Orquesta la creación de una venta delegando el cálculo a la estrategia del canal.

        Args:
            cliente_id: ID del cliente asociado a la venta.
            items: Lista de ítems [{'producto_id': int, 'cantidad': int, 'precio_unitario': float}]
            canal: Instancia concreta del canal (estrategia OCP). Si es None, usa Presencial.
            fecha: Fecha de la transacción (opcional).
        """

        detalle_ventas, subtotal_calculado = self._calcular_subtotal(items)
        total = self._resolver_estrategia(strategy=canal, subtotal=subtotal_calculado)

        self._validar_venta(
            cliente_id=cliente_id,
            items=items,
            fecha=fecha,
            total=total,
            estado=estado
        )

        # 4. Crear el modelo de dominio Venta
        nueva_venta = Venta(
            fecha=fecha,
            cliente_id=cliente_id,
            total=total,
            estado=estado,
            productos=detalle_ventas,
        )

        # 5. Persistir en la base de datos
        return self._venta_repo.insert(nueva_venta)

    def obtener_venta(self, venta_id: int) -> Venta | None:
        return self._venta_repo.get_by_id(venta_id)

    def listar_ventas(self) -> list[Venta]:
        return self._venta_repo.list_all()

    def _calcular_subtotal(self, items: list[dict]):
        subtotal_base: float = 0.0
        detalles: list[DetalleVenta] = []
        for item in items:
            subtotal_item = item["cantidad"] * item["precio_unitario"]
            subtotal_base += subtotal_item
            detalles.append(
                DetalleVenta(
                    producto_id=item["producto_id"],
                    cantidad=item["cantidad"],
                    precio_unitario=item["precio_unitario"],
                )
            )
        return detalles, subtotal_base

    def _resolver_estrategia(self, subtotal: float, strategy: CanalVentaStrategy):
        return strategy.calcular_total(subtotal=subtotal)

    def _validar_venta(
        self,
        cliente_id: int,
        items: list[dict],
        fecha: date or str,
        total: float,
        estado : str
    ):
        self._validar_productos(items)
        self._validar_cliente(cliente_id)
        self._validar_estado(estado)
        self._validar_total(total)
        self._validar_fecha(fecha)


    def _validar_fecha(self, fecha: str or date) -> None:
        if isinstance(fecha, str):
            try:
                date.fromisoformat(fecha)
            except ValueError:
                raise FechaInvalidaError()

    def _validar_cliente(self, cliente_id: int) -> None:
        pass
        #TODO

    def _validar_total(self, total: float) -> None:
        if total <= 0:
            raise TotalInvalidoError("El total debe ser mayor a 1")

    def _validar_estado(self, estado: str) -> None:
        if not isinstance(estado,str):
            raise EstadoInvalidoError("El estado de la venta no es un texto")

    def _validar_productos(self, productos: list[dict]) -> None:
        if len(productos) == 0:
            raise VentaSinProductosError("No hay productos para la venta.")
        if not isinstance(productos,list):
            raise VentaSinProductosError(
                "Los productos no satisfacen la estructura de datos requerida."
            )
        if not all(filter(lambda x: all(x.values()), productos)):
            raise VentaSinProductosError(
                "Los productos contienen valores vacios o incorrectos."
            )

