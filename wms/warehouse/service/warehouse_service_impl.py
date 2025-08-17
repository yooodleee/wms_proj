from dataclasses import dataclass
from typing import Dict, Any
from django.db import transaction
from django.core.exceptions import ValidationError

from warehouse.entity.warehouse import Warehouse
from warehouse.repository.warehouse_repository_impl import WarehouseRepositoryImpl
from warehouse.service.warehouse_service import WarehouseService


# 도메인 예외 정의
class WarehouseNotFound(Exception): ...


@dataclass
class WarehouseServiceImpl(WarehouseService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__warehouseRepository = WarehouseRepositoryImpl.getInstance()
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    

    @transaction.atomic
    def create_warehouse(self, data: Dict[str, Any]) -> Warehouse:
        if 'code' not in data or 'name' not in data:
            raise ValidationError("code와 name은 필수입니다.")
        return self.__warehouseRepository.create(data)
    
    
    @transaction.atomic
    def update_warehouse(self, warehouse_id: int, data: Dict[str, Any]) -> Warehouse:
        try:
            wh = self.__warehouseRepository.get_by_id(warehouse_id)
        except Warehouse.DoesNotExist:
            raise WarehouseNotFound("해당 창고를 찾을 수 없습니다.")
        return self.__warehouseRepository.update(wh, data)
    

    @transaction.atomic
    def delete_warehouse(self, warehouse_id: int) -> None:
        try:
            wh = self.__warehouseRepository.get_by_id(warehouse_id)
        except Warehouse.DoesNotExist:
            raise WarehouseNotFound("해당 창고를 찾을 수 없습니다.")
        return self.__warehouseRepository.delete(wh)
    

    @transaction.atomic
    def list_warehouses(self, filters: Dict[str, Any] = None):
        return self.__warehouseRepository.list(filters)