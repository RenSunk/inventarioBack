from rest_framework.views import APIView
from rest_framework.response import Response
from inventario.models import Product
from inventario.Views.ListarProductos.serializers import ProductoSerializer

class ListarProductos(APIView):
    def get(self, request):
        productos = Product.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(serializer.data)