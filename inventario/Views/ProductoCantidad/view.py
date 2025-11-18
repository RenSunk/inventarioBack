from rest_framework.views import APIView
from rest_framework.response import Response
from inventario.Views.AgregarProducto.serializers import ProductUnitSerializer
from inventario.models import ProductUnit

class ProductoCantidadView(APIView):

    def post(self, request):
        try:
            # Lógica para modificar la cantidad del producto
            product_unit_serializer = ProductUnitSerializer( data=request.data, partial=True )
            if product_unit_serializer.is_valid():
                product_unit_serializer.save()
                return Response(product_unit_serializer.data, status=200)
            else:
                return Response(product_unit_serializer.errors, status=400)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        
    def put(self, request, product_unit_id):

        try:
            # Lógica para agregar una nueva cantidad al producto
            product_unit = ProductUnit.objects.get(id=product_unit_id)
            product_unit_serializer = ProductUnitSerializer(product_unit, data=request.data, partial=True)
            if product_unit_serializer.is_valid():
                product_unit_serializer.save()
                return Response(product_unit_serializer.data, status=200)
            else:
                return Response(product_unit_serializer.errors, status=400)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        
    def get(self, request, product_unit_id):

        try:
            # Lógica para obtener la cantidad del producto
            product_unit = ProductUnit.objects.get(id=product_unit_id)
            product_unit_serializer = ProductUnitSerializer(product_unit)
            return Response(product_unit_serializer.data, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        
    def delete(self, request, product_unit_id):

        try:
            # Lógica para eliminar la cantidad del producto
            product_unit = ProductUnit.objects.get(id=product_unit_id)
            product_unit.status_id = 0
            product_unit.save()
            
            return Response({"message": f"Cantidad de producto con ID {product_unit_id} eliminada"}, status=200)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)