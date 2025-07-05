from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class Perfil(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Devuelve el perfil del usuario autenticado.
        """
        user = request.user
        if user.is_authenticated:
            perfil = {
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "picture": user.foto if hasattr(user, 'foto') and user.foto else None,
                "customer": user.cliente.nombre if hasattr(user, 'cliente') and user.cliente else None,
            }
            return Response(perfil)
        else:
            return Response({"error": "Usuario no autenticado"}, status=401)
        