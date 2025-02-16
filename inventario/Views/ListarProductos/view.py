from rest_framework.views import APIView
from rest_framework.response import Response
from inventario.models import *
from inventario.Views.ListarProductos.serializers import ProductVariantSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ListarProductos(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        user = request.user
        productos = ProductVariant.objects.filter(account=user.cliente)
        serializer = ProductVariantSerializer(productos, many=True)
        return Response(serializer.data)