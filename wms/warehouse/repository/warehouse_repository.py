from abc import ABC, abstractmethod


class WarehouseRepository(ABC):

    @abstractmethod
    def get_by_id(self, warehouse_id: int):
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def create(self, payload):
        pass

    @abstractmethod
    def update(self, warehouse, payload):
        pass

    @abstractmethod
    def delete(self, warehouse) -> None:
        pass