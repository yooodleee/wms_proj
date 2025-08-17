from abc import ABC, abstractmethod


class WarehouseService(ABC):
    
    @abstractmethod
    def create_warehouse(self, data):
        pass

    @abstractmethod
    def update_warehouse(self, warehouse_id, data):
        pass

    @abstractmethod
    def delete_warehouse(self, warehouse_id: int) -> None:
        pass

    @abstractmethod
    def list_warehouses(self, filters):
        pass