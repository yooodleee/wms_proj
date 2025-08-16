from abc import ABC, abstractmethod


class SuppliersService(ABC):

    @abstractmethod
    def create_supplier(self, data):
        pass

    @abstractmethod
    def update_supplier(self, supplier_id, changes):
        pass

    @abstractmethod
    def delete_supplier(self, supplier_id: int, *, soft=True) -> None:
        pass