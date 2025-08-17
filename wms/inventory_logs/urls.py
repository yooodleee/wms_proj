from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory_logs.controller.inventory_logs_controller import InventoryLogsController


router = DefaultRouter()
router.register(r'inventory_logs', InventoryLogsController, basename='inventory_logs')

urlpatterns = [
    path('', include(router.urls)),
]