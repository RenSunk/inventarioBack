from rest_framework import serializers
from inventario.models import *

class StockUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockUnit
        fields = '__all__'

class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'
