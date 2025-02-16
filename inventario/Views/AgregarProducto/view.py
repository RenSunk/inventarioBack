from rest_framework.views import APIView
from rest_framework.response import Response
from inventario.models import ProductVariant
from .serializers import ProductUnitSerializer, StockUnitSerializer, ProductVariantSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal


class AgregarProducto(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user

        try:
            product = ProductVariant.objects.create(
                name=data['name'],
                description=data['description'],
                account_id=user.cliente.id,
                brand=data['brand'],
            )
            product.save()

            product_unit_data = data['product_unit']
            for unit in product_unit_data:
                unit['product'] = product.id
            product_unit = ProductUnitSerializer(data=product_unit_data, many=True)
            product_unit.is_valid(raise_exception=True)
            product_unit.save()

            stock_unit_data = data['stock_unit']
            for unit in stock_unit_data:
                unit['product'] = product.id
            stock_unit = StockUnitSerializer(data=stock_unit_data, many=True)
            stock_unit.is_valid(raise_exception=True)
            stock_unit.save()

            return Response(
                ProductVariantSerializer(product).data,
                status=201
            )
        except KeyError as e:
            return Response({"error": f"Missing key: {str(e)}"}, status=400)
        except Exception as e:
            return Response({"error": str(e)}, status=500)