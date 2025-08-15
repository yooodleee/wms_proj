from rest_framework import serializers
from items.entity.items import Item


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'id', 'sku', 'name', 'category', 'unit_of_measure',
            'size', 'weight', 'barcode', 'attributes',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active']
        