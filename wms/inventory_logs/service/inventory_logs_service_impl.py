from typing import Dict, Any

from inventory_logs.entity.inventory_logs import InventoryLog
from inventory_logs.repository.inventory_logs_repository_impl import InventoryLogsRepositoryImpl
from inventory_logs.service.inventory_logs_service import InventoryLogsService

from inventory.repository.inventory_repository_impl import InventoryRepositoryImpl
from inventory.service.inventory_service_impl import InventoryServiceImpl, InventoryNotFound


class InventoryLogsServiceImpl(InventoryLogsService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__inventoryLogsRepository = InventoryLogsRepositoryImpl.getInstance()
            cls.__instance.__inventoryRepository = InventoryRepositoryImpl.getInstance()
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    

    def create_log(self, data: Dict[str, Any]) -> InventoryLog:
        """
        로그 생성 시, inventory 수량도 함께 변경
        """
        inventory_id = data.get("inventory")
        try:
            inventory = self.__inventoryRepository.get_by_id(inventory_id)
        except Exception:
            raise InventoryNotFound("해당 재고를 찾을 수 없습니다.")

        # 재고 수량 업데이트
        quantity_change = data["quantity_change"]
        inventory.quantity += quantity_change
        inventory.save()

        # 로그 기록
        return self.__inventoryLogsRepository.create(data)
    

    def list_logs(self, filters: Dict[str, Any] = None):
        return self.__inventoryLogsRepository.list(filters)