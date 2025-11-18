from rest_framework import serializers
from inventario.models import ProductVariant

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'