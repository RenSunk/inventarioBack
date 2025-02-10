from rest_framework import serializers
from inventario.models import Unit

class UnitConversionSerializer(serializers.Serializer):
    from_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    to_unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())
    value = serializers.FloatField()

    def validate(self, data):
        from_unit = data["from_unit"]
        to_unit = data["to_unit"]

        if from_unit.category != to_unit.category:
            raise serializers.ValidationError("Las unidades deben pertenecer a la misma categoría.")
        return data

    def convert(self):
        from_unit = self.validated_data["from_unit"]
        to_unit = self.validated_data["to_unit"]
        value = self.validated_data["value"]
        return from_unit.convert_to(to_unit, value)