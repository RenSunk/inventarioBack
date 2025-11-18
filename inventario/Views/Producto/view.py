from rest_framework.views import APIView
from rest_framework.response import Response
from inventario.Views.AgregarProducto.serializers import ProductVariantSerializer
from inventario.models import ProductVariant
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class ProductoView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, product_id):

        producto = ProductVariant.objects.get(id=product_id)
        # Lógica para modificar el producto

        product_variant_serializer = ProductVariantSerializer(producto, data=request.data, partial=True)
        if product_variant_serializer.is_valid():
            product_variant_serializer.save()
            return Response(product_variant_serializer.data, status=200)
        else:
            return Response(product_variant_serializer.errors, status=400)

    
    def post(self, request):
        # Lógica para crear un nuevo producto

        account = request.user.cliente
        data = request.data
        data['account'] = account.id

        product_variant_serializer = ProductVariantSerializer(data=data)

        if product_variant_serializer.is_valid():
            product_variant_serializer.save()
            return Response(product_variant_serializer.data, status=201)
        else:
            return Response(product_variant_serializer.errors, status=400)

    def delete(self, request, product_id):

        producto = ProductVariant.objects.get(id=product_id)
        
        producto.status_id = 0
        producto.save()
        
        return Response({"message": f"Producto con ID {product_id} eliminado"}, status=200)
    
    def get(self, request, product_id):

        producto = ProductVariant.objects.get(id=product_id)
        product_variant_serializer = ProductVariantSerializer(producto)

        return Response(product_variant_serializer.data, status=200)