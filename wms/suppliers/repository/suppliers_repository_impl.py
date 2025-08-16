from typing import Dict, Any, Optional
from django.db import transaction
from django.db.models import QuerySet

from suppliers.entity.suppliers import Supplier
from suppliers.repository.suppliers_repository import SuppliersRepository


class SuppliersRepositoryImpl(SuppliersRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance


    def get_by_id(self, supplier_id: int) -> Supplier:
        return Supplier.objects.get(id=supplier_id)
    

    def get_by_code(self, code: str) -> Supplier:
        return Supplier.objects.get(code=code)
    

    def exists_by_code(self, code: str) -> bool:
        return Supplier.objects.filter(code=code).exists()
    

    def list(self, filters: Optional[Dict[str, Any]] = None) -> QuerySet[Supplier]:
        qs = Supplier.objects.all()
        if not filters:
            return qs
        if 'search' in filters:
            q = filters['search']
            qs = qs.filter(name__icontains=q) | qs.filter(code__icontains=q)
        if 'is_active' in filters:
            qs = qs.filter(is_active=filters['is_active'])
        return qs
    

    @transaction.atomic
    def create(self, payload: Dict[str, Any]) -> Supplier:
        return Supplier.objects.create(**payload)
    

    @transaction.atomic
    def update(self, supplier: Supplier, changes: Dict[str, Any]) -> Supplier:
        for k, v in changes.items():
            setattr(supplier, k, v)
        supplier.save(update_fields=list(changes.keys()) + ['updated_at'])
        return supplier
    

    @transaction.atomic
    def soft_delete(self, supplier: Supplier) -> None:
        supplier.is_active = False
        supplier.save(update_fields=['is_active', 'updated_at'])


    @transaction.atomic
    def hard_delete(self, supplier: Supplier) -> None:
        supplier.delete()