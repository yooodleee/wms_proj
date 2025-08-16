from abc import ABC, abstractmethod


class SuppliersRepository(ABC):

    @abstractmethod
    def get_by_id(self, supplier_id):
        pass

    @abstractmethod
    def get_by_code(self, code):
        pass

    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def create(self, payload):
        pass

    @abstractmethod
    def update(self, supplier, changes):
        pass

    @abstractmethod
    def soft_delete(self, supplier):
        pass

    @abstractmethod
    def hard_delete(self, supplier):
        pass