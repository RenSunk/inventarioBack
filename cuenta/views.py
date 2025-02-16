from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from cuenta.models import Cuenta
from .models import *
from rest_framework import status
from .serializers import EmailTokenObtainPairSerializer
from rest_framework.views import APIView

# Create your views here.

class LoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        body = request.data
        try:
            if(serializer.is_valid(raise_exception=True)):
                if 'username' in body:
                    user = Cuenta.objects.get(username=request.data['username'], cliente=request.data['client_id'])
                else:
                    user = Cuenta.objects.get(email=request.data['email'], cliente=request.data['client_id'])
                token = serializer.get_token(user)
                response = {
                    'access_token': 'Bearer ' + str(token.access_token),
                    'lifetime': 300,
                    'username': user.username,
                    'email': user.email,
                    'password': body['password'] 
                }
                return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

