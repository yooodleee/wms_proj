from typing import Optional, Iterable, Dict, Any
from django.db import transaction
from django.db.models import QuerySet

from items.entity.items import Item
from items.repository.items_repository import ItemsRepository


class ItemsRepositoryImpl(ItemsRepository):
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
    
    def get_by_id(self, item_id: int) -> Item:
        return Item.objects.get(id=item_id)
    
    def get_by_sku(self, sku: str) -> Item:
        return Item.objects.get(sku=sku)
    
    def exists_by_sku(self, sku: str) -> bool:
        return Item.objects.filter(sku=sku).exists()
    
    def list(self, filters: Optional[Dict[str, Any]] = None) -> QuerySet[Item]:
        qs = Item.objects.all()
        if not filters:
            return qs
        if 'search' in filters:
            q = filters['search']
            qs = qs.filter(name__icontains=q) | qs.filter(sku__icontains=q)
        if 'category' in filters:
            qs = qs.filter(category=filters['category'])
        if 'is_active' in filters:
            qs = qs.filter(is_active=filters['is_active'])
        if 'barcode' in filters:
            qs = qs.filter(barcode=filters['barcode'])
        return qs
    
    @transaction.atomic
    def create(self, payload: Dict[str, Any]) -> Item:
        return Item.objects.create(**payload)
    
    @transaction.atomic
    def update(self, item: Item, changes: Dict[str, Any]) -> Item:
        for k, v in changes.items():
            setattr(item, k, v)
        item.save(update_fields=list(changes.keys()) + ['updated_at'])
        return item
    
    @transaction.atomic
    def soft_delete(self, item: Item) -> None:
        item.is_active = False
        item.save(update_fields=['is_active', 'updated_at'])
    
    @transaction.atomic
    def hard_delete(self, item: Item) -> None:
        item.delete()