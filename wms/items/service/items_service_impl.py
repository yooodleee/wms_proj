from dataclasses import dataclass
from typing import Dict, Any, Optional
from django.db import transaction
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from items.service.items_service import ItemsService
from items.repository.items_repository_impl import ItemsRepositoryImpl
from items.entity.items import Item

# 도메인 예외 정의
class ItemAlreadyExists(Exception): ...
class ItemNotFound(Exception): ...


@dataclass
class ItemsServiceImpl(ItemsService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__itemsRepository = ItemsRepositoryImpl.getInstance()
        
        return cls.__instance
    
    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    
    @transaction.atomic
    def create_item(self, data: Dict[str, Any]) -> Item:
        sku = data.get('sku')
        name = data.get('name')

        if not sku or not name: 
            raise ValueError("sku와 name은 필수입니다.")
        if self.__itemsRepository.exists_by_sku(sku):
            raise ItemAlreadyExists(f"이미 존재하는 sku입니다: {sku}")
        
        # 추가 비즈니스 규칙: weight >= 0
        weight = data.get('weight')
        if weight is not None and float(weight) < 0:
            raise ValidationError("weight는 0 이상이어야 합니다.")
        
        return self.__itemsRepository.create(data)
    
    @transaction.atomic
    def update_item(self, item_id: int, changes: Dict[str, Any]) -> Item:
        try:
            item = self.__itemsRepository.get_by_id(item_id)
        except ObjectDoesNotExist:
            raise ItemNotFound(f"item_id={item_id}를 찾을 수 없습니다.")
        
        # sku 변경 시 unique 보장
        new_sku = changes.get('sku')
        if new_sku and new_sku != item.sku and self.__itemsRepository.exists_by_sku(new_sku):
            raise ItemAlreadyExists(f"이미 존재하는 sku입니다: {new_sku}")
        
        weight = changes.get('weight')
        if weight is not None and float(weight) < 0:
            raise ValidationError("weight는 0 이상이어야 합니다.")
        
        return self.__itemsRepository.update(item, changes)
    
    @transaction.atomic
    def delete_item(self, item_id: int, *, soft: bool = True) -> None:
        try:
            item = self.__itemsRepository.get_by_id(item_id)
        except ObjectDoesNotExist:
            raise ItemNotFound(f"item_id={item_id}를 찾을 수 없습니다.")
        
        # 인벤토리 존재/연결 검증 등 비즈니스 제약 추가 기능
        if soft:
            self.__itemsRepository.soft_delete(item)
        else:
            self.__itemsRepository.hard_delete(item)