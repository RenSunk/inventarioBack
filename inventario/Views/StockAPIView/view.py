from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StockOperationSerializer

class StockAPIView(APIView):
    def post(self, request, operation ):
        """
        operation: "add" o "remove"
        """
        serializer = StockOperationSerializer(data=request.data)
        if serializer.is_valid():
            try:
                if operation == "add":
                    serializer.add_stock()
                elif operation == "remove":
                    serializer.remove_stock()
                else:
                    return Response({"error": "Operación no válida."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Operación realizada con éxito."}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
