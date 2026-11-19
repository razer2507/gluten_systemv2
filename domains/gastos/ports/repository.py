from abc import ABC, abstractmethod

from domains.gastos.models import Gasto


class GastosRepository(ABC):
    @abstractmethod
    def insert(self, gasto: Gasto) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Gasto]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Gasto | None:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Gasto]:
        pass

    @abstractmethod
    def update(self, gasto: Gasto) -> None:
        pass

    @abstractmethod
    def delete(self, gasto: Gasto) -> None:
        pass
