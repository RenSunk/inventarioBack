from inventario.models import Unit
from .serializers import UnitSerializer
from rest_framework.viewsets import ModelViewSet

class CantidadesView(ModelViewSet):
    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    ordering = ['id']
