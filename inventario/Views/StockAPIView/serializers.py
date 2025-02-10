from rest_framework import serializers
from inventario.models import Product, Unit

class StockOperationSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    unit_id = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    quantity = serializers.FloatField()

    def validate(self, data):
        product = data["product_id"]
        unit = data["unit_id"]

        if product.base_unit.category != unit.category:
            raise serializers.ValidationError("La unidad no corresponde a la categoría del producto.")
        return data

    def add_stock(self):
        product = self.validated_data["product_id"]
        unit = self.validated_data["unit_id"]
        quantity = self.validated_data["quantity"]
        product.add_stock(quantity, unit)

    def remove_stock(self):
        product = self.validated_data["product_id"]
        unit = self.validated_data["unit_id"]
        quantity = self.validated_data["quantity"]
        product.remove_stock(quantity, unit)
