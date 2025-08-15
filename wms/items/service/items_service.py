from abc import ABC, abstractmethod


class ItemsService(ABC):

    @abstractmethod
    def create_item(self, data):
        pass

    @abstractmethod
    def update_item(self, item_id: int, changes):
        pass

    @abstractmethod
    def delete_item(self, item_id: int, *, soft: bool = True) -> None:
        pass
    