from rest_framework import serializers
from inventory.entity.inventory import Inventory


class InventorySerializer(serializers.ModelSerializer):
    warehouse_name = serializers.CharField(source="warehouse.name", read_only=True)
    item_name = serializers.CharField(source="item.name", read_only=True)

    class Meta:
        models = Inventory
        fields = [
            "id", "warehouse", "warehouse_name", "item", "item_name", "quantity",
            "lot_number", "expiration_date", "created_at", "updated_at"
        ]