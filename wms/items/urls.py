from django.urls import path, include
from rest_framework.routers import DefaultRouter

from items.controller.items_controller import ItemsController


router = DefaultRouter()
router.register(r"items", ItemsController, basename='items')

urlpatterns = [
    path('', include(router.urls)),
]