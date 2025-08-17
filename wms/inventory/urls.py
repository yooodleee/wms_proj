from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.controller.inventory_controller import InventoryController


router = DefaultRouter()
router.register(r'inventory', InventoryController, basename='inventory')

urlpatterns = [
    path('', include(router.urls)),
]