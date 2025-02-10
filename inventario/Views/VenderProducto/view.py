from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from inventario.models import *

class VenderProducto(APIView):
    def post(self, request):
        data = request.data

        quantity = data['quantity']
        stock_id = data['stock_id']
        unit_id = data['unit_id']
        Product.objects.get(id=data['producto_id']).remove_stock(
            Decimal(quantity), stock_id, unit_id
        )
        
        return Response({"message": "Operación realizada con éxito."}, status=status.HTTP_200_OK)


