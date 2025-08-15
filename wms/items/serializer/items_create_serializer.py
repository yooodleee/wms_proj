from rest_framework import serializers
from items.entity.items import Item


class ItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            'sku', 'name', 'category', 'unit_of_measure',
            'size', 'weight', 'barcode', 'attributes'
        ]
        