from abc import ABC, abstractmethod


class InventoryLogsRepository(ABC):

    @abstractmethod
    def get_by_id(self, log_id: int):
        pass

    @abstractmethod
    def list(self, filters):
        pass

    @abstractmethod
    def create(self, payload):
        pass