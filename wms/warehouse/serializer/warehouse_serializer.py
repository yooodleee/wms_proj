from rest_framework import serializers
from warehouse.entity.warehouse import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = [
            'id', 'code', 'name', 'location', 'is_active', 'created_at', 'updated_at'
        ]