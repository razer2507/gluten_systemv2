from abc import ABC, abstractmethod

from domains.productos.models import Producto


class ProductosRepository(ABC):
    @abstractmethod
    def insert(self, producto: Producto) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Producto]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Producto | None:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Producto]:
        pass

    @abstractmethod
    def update(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def delete(self, producto: Producto) -> None:
        pass
