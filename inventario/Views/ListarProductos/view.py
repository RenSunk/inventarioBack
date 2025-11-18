from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventario.models import *
from inventario.Views.ListarProductos.serializers import ProductVariantSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class ListarProductos(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get(self, request):

        nombre = request.query_params.get("name", "")

        user = request.user
        productos = ProductVariant.objects.filter(
            name__icontains=nombre, account=user.cliente, status=1
        ).order_by("id")
        
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(productos, request)

        if paginated_queryset is not None:
            serializer = ProductVariantSerializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            serializer = ProductVariantSerializer(productos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
