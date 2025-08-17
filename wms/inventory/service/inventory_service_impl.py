from typing import Dict, Any
from django.core.exceptions import ValidationError

from inventory.entity.inventory import Inventory
from inventory.repository.inventory_repository_impl import InventoryRepositoryImpl
from inventory.service.inventory_service import InventoryService


# 도메인 예외 정의
class InventoryNotFound(Exception): ...


class InventoryServiceImpl(InventoryService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__inventoryRepository = InventoryRepositoryImpl.getInstance()
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    

    def create_inventory(self, data: Dict[str, Any]) -> Inventory:
        if "warehouse" not in data or "item" not in data:
            raise ValidationError("warehouse와 item은 필수입니다.")
        return self.__inventoryRepository.create(data)
    

    def update_inventory(self, inventory_id: int, data: Dict[str, Any]) -> Inventory:
        try:
            inv = self.__inventoryRepository.get_by_id(inventory_id)
        except Inventory.DoesNotExist:
            raise InventoryNotFound("해당 재고를 찾을 수 없습니다.")
        return self.__inventoryRepository.update(inv, data)
    

    def delete_inventory(self, inventory_id: int) -> None:
        try:
            inv = self.__inventoryRepository(inventory_id)
        except Inventory.DoesNotExist:
            raise InventoryNotFound("해당 재고를 찾을 수 없습니다.")
        self.__inventoryRepository.delete(inv)
    

    def list_inventories(self, filters: Dict[str, Any] = None):
        return self.__inventoryRepository.list(filters)