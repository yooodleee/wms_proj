from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from suppliers.repository.suppliers_repository_impl import SuppliersRepositoryImpl
from suppliers.service.suppliers_service_impl import SuppliersServiceImpl, SupplierAlreadyExists, SupplierNotFound

from suppliers.serializer.suppliers_serializer import SuppliersSerializer
from suppliers.serializer.suppliers_create_serializer import SuppliersCreateSerializer
from suppliers.serializer.suppliers_update_serializer import SuppliersUpdateSerializer


class SuppliersController(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    api/suppliers/ (GET, POST)
    api/suppliers/{id} (GET, PUT/PATCH, DELETE)
    """
    queryset = SuppliersRepositoryImpl().list()
    serializer_class = SuppliersSerializer

    # 간단한 의존성 구성 
    repo = SuppliersRepositoryImpl()
    service = SuppliersServiceImpl()

    
    def list(self, request, *args, **kwargs):
        params = {
            'search': request.query_params.get('search'),
            'is_active': request.query_params.get('is_active')
        }
        if params['is_active'] is not None:
            params['is_active'] = params['is_active'].lower() in ['true', '1', 't', 'yes']
        
        qs = self.repo.list(filters=params)
        page = self.paginate_queryset(qs)
        ser = SuppliersSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)
    

    def retrieve(self, request, pk=None, *args, **kwargs):
        supplier = self.repo.get_by_id(pk)
        return Response(SuppliersSerializer(supplier).data)
    
    
    def create(self, request, *args, **kwargs):
        ser = SuppliersCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            supplier = self.service.create_supplier(ser.validated_data)
        except SupplierAlreadyExists as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(SuppliersSerializer(supplier).data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk=None, *args, **kwargs):
        partial = request.method.lower() == 'patch'
        ser = SuppliersUpdateSerializer(data=request.data, partial=partial)
        ser.is_valid(raise_exception=True)
        try:
            supplier = self.service.update_supplier(int(pk), ser.validated_data)
        except SupplierNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except SupplierAlreadyExists as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)
        return Response(SuppliersSerializer(supplier).data)
    

    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)
    

    def destroy(self, request, pk=None, *args, **kwargs):
        soft = request.query_params.get('soft', 'true').lower() in ['true', '1', 't', 'yes']
        try:
            self.service.delete_supplier(int(pk), soft=soft)
        except SupplierNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    