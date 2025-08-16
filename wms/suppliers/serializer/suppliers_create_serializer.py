from rest_framework import serializers
from suppliers.entity.suppliers import Supplier


class SuppliersCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['code', 'name', 'contact_name', 'phone', 'email', 'address']

        