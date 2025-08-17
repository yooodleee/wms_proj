from rest_framework import status, viewsets
from rest_framework.response import Response

from inventory.repository.inventory_repository_impl import InventoryRepositoryImpl
from inventory.service.inventory_service_impl import InventoryServiceImpl, InventoryNotFound
from inventory.serializer.inventory_serializer import InventorySerializer


class InventoryController(viewsets.ViewSet):
    repo = InventoryRepositoryImpl()
    service = InventoryServiceImpl()

    def list(self, request):
        filters = {
            "warehouse_id": request.query_params.get("warehouse_id"),
            "item_id": request.query_params.get("item_id"),
        }
        qs = self.service.list_inventories(filters)
        return Response(InventorySerializer(qs, many=True).data)
    

    def create(self, request):
        ser = InventorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        inv = self.service.create_inventory(ser.validated_data)
        return Response(InventorySerializer(inv).data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk=None):
        ser = InventorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            inv = self.service.update_inventory(pk, ser.validated_data)
        except InventoryNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(InventorySerializer(inv).data)
    

    def destroy(self, request, pk=None):
        try:
            self.service.delete_inventory(pk)
        except InventoryNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)