

from abc import ABC, abstractmethod


class ClientesRepository(ABC):
    @abstractmethod
    def _get_conn(self):
        pass

    @abstractmethod
    def insert(self, cliente) -> int:
        pass

    @abstractmethod
    def get_all(self) -> list:
        pass

    @abstractmethod
    def get_by_id(self, id) -> dict:
        pass

    @abstractmethod
    def get_filtered(self, **kwargs) -> list:
        pass

    @abstractmethod
    def delete(self, cliente) -> dict:
        pass

    @abstractmethod
    def update(self, cliente) -> None:
        pass
