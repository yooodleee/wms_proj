from rest_framework import status, viewsets
from rest_framework.response import Response

from warehouse.repository.warehouse_repository_impl import WarehouseRepositoryImpl
from warehouse.service.warehouse_service_impl import WarehouseServiceImpl, WarehouseNotFound
from warehouse.serializer.warehouse_serializer import WarehouseSerializer


class WarehouseController(viewsets.ViewSet):
    """
    api/warehouse/ (GET, POST)
    api/warehouse/{id} (GET, PUT/PATCH, DELETE)
    """
    repo = WarehouseRepositoryImpl()
    service = WarehouseServiceImpl()

    def list(self, request):
        qs = self.service.list_warehouses()
        return Response(WarehouseSerializer(qs, many=True).data)
    

    def create(self, request):
        ser = WarehouseSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        wh = self.service.create_warehouse(ser.validated_data)
        return Response(WarehouseSerializer(wh).data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk=None):
        ser = WarehouseSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            wh = self.service.update_warehouse(pk, ser.validated_data)
        except WarehouseNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(WarehouseSerializer(wh).data)
    

    def destroy(self, request, pk=None):
        try:
            self.service.delete_warehouse(pk)
        except WarehouseNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)