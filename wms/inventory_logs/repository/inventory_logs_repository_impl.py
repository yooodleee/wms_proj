from typing import Optional, Dict, Any
from django.db.models import QuerySet

from inventory_logs.entity.inventory_logs import InventoryLog
from inventory_logs.repository.inventory_logs_repository import InventoryLogsRepository


class InventoryLogsRepositoryImpl(InventoryLogsRepository):
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
    

    def get_by_id(self, log_id: int) -> InventoryLog:
        return InventoryLog.objects.get(id=log_id)
    

    def list(self, filters: Optional[Dict[str, Any]] = None) -> QuerySet[InventoryLog]:
        qs = InventoryLog.objects.select_related("inventory_warehouse", "inventory_item").all()
        if filters:
            if "inventory_id" in filters:
                qs = qs.filter(inventory_id=filters["inventory_id"])
            if "action_type" in filters:
                qs = qs.filter(action_type=filters["action_type"])
        return qs
    

    def create(self, payload: Dict[str, Any]) -> InventoryLog:
        return InventoryLog.objects.create(**payload)