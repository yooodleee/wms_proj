from django.urls import path, include
from rest_framework.routers import DefaultRouter

from warehouse.controller.warehouse_controller import WarehouseController


router = DefaultRouter()
router.register(r'warehouse', WarehouseController, basename='warehouse')

urlpatterns = [
    path('', include(router.urls)),
]