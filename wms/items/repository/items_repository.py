from abc import ABC, abstractmethod


class ItemsRepository(ABC):
    
    @abstractmethod
    def get_by_id(self, item_id: int):
        pass

    @abstractmethod
    def get_by_sku(self, sku: str):
        pass

    @abstractmethod
    def exists_by_sku(self, sku: str) -> bool:
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def create(self, payload):
        pass

    @abstractmethod
    def update(self, item, changes):
        pass

    @abstractmethod
    def soft_delete(self, item) -> None:
        pass

    @abstractmethod
    def hard_delete(self, item) -> None:
        pass