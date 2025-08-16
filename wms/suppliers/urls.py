from django.urls import path, include
from rest_framework.routers import DefaultRouter
from suppliers.controller.suppliers_controller import SuppliersController


router = DefaultRouter()
router.register(r'suppliers', SuppliersController, basename='suppliers')

urlpatterns = [
    path('', include(router.urls)),
]