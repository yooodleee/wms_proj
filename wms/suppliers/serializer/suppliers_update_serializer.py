from rest_framework import serializers
from suppliers.entity.suppliers import Supplier


class SuppliersUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = [
            'code', 'name', 'contact_name', 'phone',
            'email', 'address', 'is_active'
        ]

        