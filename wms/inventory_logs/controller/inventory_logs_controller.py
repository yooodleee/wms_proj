from rest_framework import status, viewsets
from rest_framework.response import Response

from inventory_logs.repository.inventory_logs_repository_impl import InventoryLogsRepositoryImpl
from inventory_logs.service.inventory_logs_service_impl import InventoryLogsServiceImpl
from inventory_logs.serializer.inventory_logs_serializer import InventoryLogsSerializer

from inventory.repository.inventory_repository_impl import InventoryRepositoryImpl


class InventoryLogsController(viewsets.ViewSet):
    repo = InventoryLogsRepositoryImpl()
    inventory_repo = InventoryRepositoryImpl()
    service = InventoryLogsServiceImpl()

    def list(self, request):
        filters = {
            "inventory_id": request.query_params.get("inventory_id"),
            "action_type": request.query_params.get("action_type"),
        }
        qs = self.service.list_logs(filters)
        return Response(InventoryLogsSerializer(qs, many=True).data)

    
    def create(self, request):
        ser = InventoryLogsSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        log = self.service.create_log(ser.validated_data)
        return Response(InventoryLogsSerializer(log).data, status=status.HTTP_201_CREATED)