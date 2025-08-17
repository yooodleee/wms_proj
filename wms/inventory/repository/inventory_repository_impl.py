from typing import Optional, Dict, Any
from django.db.models import QuerySet

from inventory.entity.inventory import Inventory
from inventory.repository.inventory_repository import InventoryRepository


class InventoryRepositoryImpl(InventoryRepository):
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
    

    def get_by_id(self, inventory_id: int) -> Inventory:
        return Inventory.objects.get(id=inventory_id)
    
    
    def list(self, filters: Optional[Dict[str, Any]] = None) -> QuerySet[Inventory]:
        qs = Inventory.objects.select_related("warehouse", "item").all()
        if filters:
            if "warehouse_id" in filters:
                qs = qs.filter(warehouse_id=filters["warehouse_id"])
            if "item_id" in filters:
                qs = qs.filter(item_id=filters["item_id"])
        return qs
    

    def create(self, payload: Dict[str, Any]) -> Inventory:
        return Inventory.objects.create(**payload)
    

    def update(self, inventory: Inventory, payload: Dict[str, Any]) -> Inventory:
        for field, value in payload.items():
            setattr(inventory, field, value)
        inventory.save()
        return inventory
    

    def delete(self, inventory: Inventory) -> None:
        inventory.delete()
        return inventory