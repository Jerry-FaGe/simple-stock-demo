from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Good
from .serializers import GoodSerializer
from .utils.cache import GoodCacheManager
from .services import GoodReserveService
from .exceptions import StockException


class GoodListView(APIView):
    def get(self, request):  # noqa: ignore static method warning
        page_size = 10
        # 构建缓存键
        params = {
            "name": request.query_params.get('name', 'all'),
            "page": request.query_params.get('page', 1),
            "page_size": request.query_params.get('page_size', page_size)
        }

        cache_data = GoodCacheManager.get_list(params)
        if cache_data:
            return Response(cache_data)

        if params["name"] == "all":
            goods = Good.objects.all()
        else:
            goods = Good.objects.filter(name__icontains=params["name"])

        # 分页
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_goods = paginator.paginate_queryset(goods, request)

        serializer = GoodSerializer(paginated_goods, many=True)
        data = paginator.get_paginated_response(serializer.data).data

        # 写入缓存
        if data.get('results'):
            GoodCacheManager.set_list(params, data)

        return paginator.get_paginated_response(serializer.data)

class GoodDetailView(APIView):
    def get(self, request, pk: int):  # noqa: ignore static method warning
        cache_data = GoodCacheManager.get_detail(pk)
        if cache_data:
            if GoodCacheManager.is_null_cache(cache_data):
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(cache_data)

        try:
            good = Good.objects.get(pk=pk)
        except Good.DoesNotExist:
            GoodCacheManager.set_null_detail(pk)
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GoodSerializer(good)
        GoodCacheManager.set_detail(pk, serializer.data)
        return Response(serializer.data)

class GoodReserveView(APIView):
    def post(self, request, pk):  # noqa: ignore static method warning
        count = request.data.get('count')

        if not isinstance(count, int) or count <= 0:
            return Response("无效的数量", status=status.HTTP_400_BAD_REQUEST)

        try:
            success, remaining = GoodReserveService().reserve(pk, count)

            if success:
                return Response(f"下单成功，剩余数量为 {remaining}", status=status.HTTP_200_OK)
            return Response(f"下单失败，剩余数量为 {remaining}", status=status.HTTP_409_CONFLICT)

        except StockException as e:
            return Response(e.detail, status=e.status_code)
