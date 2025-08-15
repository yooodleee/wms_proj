from rest_framework import status, mixins, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from items.repository.items_repository_impl import ItemsRepositoryImpl
from items.service.items_service_impl import ItemsServiceImpl, ItemAlreadyExists, ItemNotFound
from items.serializer.items_serializer import ItemsSerializer
from items.serializer.items_create_serializer import ItemsCreateSerializer
from items.serializer.item_update_serializer import ItemsUpdateSerializer


@method_decorator(never_cache, name='dispatch')
class ItemsController(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """
    items/ (GET, POST)
    items/{id} (GET, PUT/PATCH, DELETE)
    """
    queryset = ItemsRepositoryImpl().list()
    serializer_class = ItemsSerializer

    # 간단한 의존성 구성
    repo = ItemsRepositoryImpl()
    service = ItemsServiceImpl()

    def list(self, request, *args, **kwargs):
        params = {
            'search': request.query_params.get('search'),
            'category': request.query_params.get('category'),
            'is_active': request.query_params.get('is_active'),
            'barcode': request.query_params.get('barcode'),
        }
        # str -> bool 캐스팅
        if params['is_active'] is not None:
            params['is_active'] = params['is_active'].lower() in ['true', '1', 't', 'yes']
        
        qs = self.repo.list(filters=params)
        page = self.paginate_queryset(qs)
        ser = ItemsSerializer(page or qs, many=True)
        if page is not None:
            return self.get_paginated_response(ser.data)
        return Response(ser.data)
    

    def retrieve(self, request, pk=None, *args, **kwargs):
        item = self.repo.get_by_id(pk)
        return Response(ItemsSerializer(item).data)
    

    def create(self, request, *args, **kwargs):
        ser = ItemsCreateSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            item = self.service.create_item(data=request.data)
        except ItemAlreadyExists as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemsSerializer(item).data, status=status.HTTP_201_CREATED)
    

    def update(self, request, pk=None, *args, **kwargs):
        partial = request.method.lower() == 'patch'
        ser = ItemsUpdateSerializer(data=request.data, partial=partial)
        ser.is_valid(raise_exception=True)
        try:
            item = self.service.update_item(int(pk), ser.validated_data)
        except ItemNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except ItemAlreadyExists as e:
            return Response({'detail': str(e)}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ItemsSerializer(item).data)
    

    def partial_update(self, request, pk=None, *args, **kwargs):
        return self.update(request, pk, *args, **kwargs)
    

    def destroy(self, request, pk=None, *args, **kwargs):
        soft = request.query_params.get('soft', 'true').lower() in ['true', '1', 't', 'yes']
        try:
            self.service.delete_item(int(pk), soft=soft)
        except ItemNotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @action(methods=['post'], detail=False, url_path='bulk-create')
    def bulk_create(self, request):
        """
        (Options) 대량 등록: [{...}, {...}]
        트랜잭션으로 처리.
        """
        created = []
        errors = []

        for row in request.data:
            ser = ItemsCreateSerializer(data=row)
            if not ser.is_valid():
                errors.append({'input': row, 'error': ser.errors})
                continue
            try:
                created.append(self.service.create_item(ser.validated_data))
            except Exception as e:
                errors.append({'input': row, 'error': str(e)})
        return Response({
            'created': ItemsSerializer(created, many=True).data,
            'errors': errors
        }, status=status.HTTP_207_MULTI_STATUS)
    
    