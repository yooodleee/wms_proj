from dataclasses import dataclass
from typing import Dict, Any
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from suppliers.entity.suppliers import Supplier
from suppliers.repository.suppliers_repository_impl import SuppliersRepositoryImpl
from suppliers.service.suppliers_service import SuppliersService


# 도메인 예외 정의 
class SupplierAlreadyExists(Exception): ...
class SupplierNotFound(Exception): ...


@dataclass
class SuppliersServiceImpl(SuppliersService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__suppliersRepository = SuppliersRepositoryImpl.getInstance()
        
        return cls.__instance
    

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        
        return cls.__instance
    
    
    @transaction.atomic
    def create_supplier(self, data: Dict[str, Any]) -> Supplier:
        code = data.get('code')
        name = data.get('name')
        
        if not code or not name:
            raise ValidationError("code와 name은 필수입니다.")
        if self.__suppliersRepository.exists_by_code(code):
            raise SupplierAlreadyExists(f"이미 존재하는 code입니다: {code}")
        return self.__suppliersRepository.create(data)
    

    @transaction.atomic
    def update_supplier(self, supplier_id: int, changes: Dict[str, Any]) -> Supplier:
        try:
            supplier = self.__suppliersRepository.get_by_id(supplier_id)
        except ObjectDoesNotExist:
            raise SupplierNotFound(f"id={supplier_id}를 찾을 수 없습니다.")

        new_code = changes.get('code')
        if new_code and new_code != supplier.code and self.__suppliersRepository.exists_by_code(new_code):
            raise SupplierAlreadyExists(f"이미 존재하는 code입니다: {new_code}")
        
        return self.__suppliersRepository.update(supplier, changes)
    

    @transaction.atomic
    def delete_supplier(self, supplier_id: int, *, soft=True) -> None:
        try:
            supplier = self.__suppliersRepository.get_by_id(supplier_id)
        except ObjectDoesNotExist:
            raise SupplierNotFound(f"id={supplier_id}를 찾을 수 없습니다.")
        
        if soft:
            self.__suppliersRepository.soft_delete(supplier)
        else:
            self.__suppliersRepository.hard_delete(supplier)