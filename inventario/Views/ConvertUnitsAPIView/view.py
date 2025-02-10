from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UnitConversionSerializer

class ConvertUnitsAPIView(APIView):
    def post(self, request):
        serializer = UnitConversionSerializer(data=request.data)
        if serializer.is_valid():
            converted_value = serializer.convert()
            return Response({"converted_value": converted_value}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)