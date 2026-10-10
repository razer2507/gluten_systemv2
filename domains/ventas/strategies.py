from abc import ABC, abstractmethod


class CanalVentaStrategy(ABC):
    """Contrato base para el cálculo de totales según el canal."""

    @abstractmethod
    def calcular_total(self, subtotal: float) -> float:
        pass


class CanalPresencialStrategy(CanalVentaStrategy):
    """Venta directa en tienda (sin recargos adicionales)."""

    def calcular_total(self, subtotal: float) -> float:
        return subtotal


class CanalPedidosYaStrategy(CanalVentaStrategy):
    """Aplica una comisión/recargo por servicio de delivery PedidosYa (20%)."""

    def __init__(self,porcentaje:float = 20.0) -> None:
        self.descuento = (porcentaje/100)
    
    def calcular_total(self, subtotal: float) -> float:
        return subtotal - (subtotal * self.descuento)


