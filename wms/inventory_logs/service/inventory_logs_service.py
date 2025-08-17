from abc import ABC, abstractmethod


class InventoryLogsService(ABC):

    @abstractmethod
    def create_log(self, data):
        pass

    @abstractmethod
    def list_logs(self, filters):
        pass