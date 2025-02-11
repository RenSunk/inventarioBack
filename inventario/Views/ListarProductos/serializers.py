from rest_framework import serializers
from inventario.models import *

class StockUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUnit
        fields = '__all__'

class ConversionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversionCategory
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    category = ConversionCategorySerializer()
    class Meta:
        model = Unit
        fields = '__all__'

class ProductUnitSerializer(serializers.ModelSerializer):
    unit = UnitSerializer()
    class Meta:
        model = ProductUnit
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    units = ProductUnitSerializer(many=True, read_only=True)
    stock_units = StockUnitSerializer(many=True, read_only=True)
    total_stock = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        