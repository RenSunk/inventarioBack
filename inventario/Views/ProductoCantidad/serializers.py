from rest_framework import serializers
from inventario.models import ProductUnit

class ProductUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = '__all__'