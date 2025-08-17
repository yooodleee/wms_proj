from abc import ABC, abstractmethod


class InventoryRepository(ABC):

    @abstractmethod
    def get_by_id(self, inventory_id: int):
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def create(self, payload):
        pass

    @abstractmethod
    def update(self, inventory):
        pass

    @abstractmethod
    def delete(self, inventory):
        pass