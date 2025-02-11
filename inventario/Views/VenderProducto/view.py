from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventario.models import *

class VenderProducto(APIView):
    def post(self, request):
        data = request.data

        quantity = data['quantity']
        stock_id = data['stock_id'] if 'stock_id' in data else None
        unit_id = data['unit_id']
        
        return Product.objects.get(id=data['producto_id']).remove_stock(
            Decimal(quantity), stock_id, unit_id
        )


