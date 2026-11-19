from abc import ABC, abstractmethod

from domains.ventas.models import Venta


class VentasRepository(ABC):
    @abstractmethod
    def insert(self, venta: Venta) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Venta]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Venta | None:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Venta]:
        pass

    @abstractmethod
    def delete(self, venta: Venta) -> None:
        pass

    @abstractmethod
    def update(self, venta: Venta) -> None:
        pass
