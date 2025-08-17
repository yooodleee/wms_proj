from django.db import models
from inventory.entity.inventory import Inventory


class InventoryLog(models.Model):
    """
    재고 변경 로그(Entity).
    입고, 출고, 조정 등 재고 변화를 기록
    """
    class ActionType(models.TextChoices):
        INBOUND = "INBOUND", "입고"
        OUTBOUND = "OUTBOUND", "출고"
        ADJUSTMENT = "ADJUSTMENT", "조정"
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='inventory_logs')

    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    quantity_change = models.IntegerField() # 양수=입고, 음수=출고
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inventory_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.action_type}] {self.inventory.item.name} @ {self.inventory.warehouse.code} ({self.quantity_change})"