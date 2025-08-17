from django.db import models

from items.entity.items import Item
from warehouse.entity.warehouse import Warehouse


class Inventory(models.Model):
    """
    재고 상태(Entity)
    특정 창고에 특정 아이템이 몇 개 있는지 관리
    """
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='inventory')

    quantity = models.PositiveIntegerField(default=0)
    log_number = models.CharField(max_length=64, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'inventory'
        unique_together = ("warehouse", "item", "log_number", "expiration_date")
        ordering = ['warehouse', 'item']
    
    def __str__(self):
        return f"{self.item.name} @ {self.warehouse.code} - {self.quantity}"