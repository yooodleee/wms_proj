from typing import Optional, Dict, Any
from django.db.models import QuerySet

from warehouse.entity.warehouse import Warehouse
from warehouse.repository.warehouse_repository import WarehouseRepository


class WarehouseRepositoryImpl(WarehouseRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    

    def get_by_id(self, warehouse_id: int) -> Warehouse:
        return Warehouse.objects.filter(id=warehouse_id)
    

    def list(self, filters: Optional[Dict[str, Any]] = None) -> QuerySet[Warehouse]:
        qs = Warehouse.objects.all()
        if filters and 'is_active' in filters:
            qs = qs.filter(is_active=filters['is_active'])
        return qs
    

    def create(self, payload: Dict[str, Any]) -> Warehouse:
        return Warehouse.objects.create(**payload)
    

    def update(self, warehouse: Warehouse, payload: Dict[str, Any]) -> Warehouse:
        for field, value in payload.items():
            setattr(warehouse, field, value)
        warehouse.save()
        return warehouse
    

    def delete(self, warehouse: Warehouse) -> None:
        warehouse.delete()