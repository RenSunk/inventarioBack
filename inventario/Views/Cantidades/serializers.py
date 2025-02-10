from rest_framework import serializers
from inventario.models import Unit

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category'] = instance.category.name
        data["complete_name"] = data["name"] + " (" + data["category"] + ")"
        return data