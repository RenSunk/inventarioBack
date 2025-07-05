from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventario.models import *

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class VenderProducto(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        data = request.data
        for item in data:
            ProductVariant.objects.get(id=item['producto_id']).remove_stock(
                Decimal(item['quantity']), item['stock_id'] if 'stock_id' in item else None, item['unit_id']
            )


