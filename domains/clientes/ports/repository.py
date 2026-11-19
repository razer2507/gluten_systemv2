from abc import ABC, abstractmethod

from domains.clientes.models import Cliente


class ClientesRepository(ABC):
    @abstractmethod
    def insert(self, cliente: Cliente) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list[Cliente]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Cliente | None:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list[Cliente]:
        pass

    @abstractmethod
    def delete(self, cliente: Cliente) -> None:
        pass

    @abstractmethod
    def update(self, cliente: Cliente) -> None:
        pass
