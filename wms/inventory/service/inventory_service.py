from abc import ABC, abstractmethod


class InventoryService(ABC):

    @abstractmethod
    def create_inventory(self, data):
        pass

    @abstractmethod
    def update_inventory(self, inventory_id: int, data):
        pass

    @abstractmethod
    def delete_inventory(self, inventory_id: int) -> None:
        pass

    @abstractmethod
    def list_inventories(self, filters):
        pass