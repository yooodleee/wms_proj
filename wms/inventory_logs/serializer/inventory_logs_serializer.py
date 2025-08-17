from rest_framework import serializers
from inventory_logs.entity.inventory_logs import InventoryLog


class InventoryLogsSerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source="inventory.warehouse.name", read_only=True)
    item_name = serializers.CharField(source="inventory.item.name", read_only=True)

    class Meta:
        model = InventoryLog
        fields = [
            "id", "inventory", "warehouse_name", "item_name",
            "action_type", "quantity_change", "description", "created_at"
        ]