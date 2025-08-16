from rest_framework import serializers
from suppliers.entity.suppliers import Supplier


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'id', 'code', 'name', 'contact_name', 'phone', 'email',
            'address', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_active']

        