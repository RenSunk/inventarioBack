from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from cuenta.models import Cuenta

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Agregar datos personalizados al token
        token['username'] = user.username
        return token

    def is_valid(self, raise_exception=False):
        attrs = self.initial_data

        # Autenticación basada en email
        if "email" not in attrs:
            user = Cuenta.objects.filter(username=attrs['username'], cliente=attrs['client_id']).first()
        else:
            user = Cuenta.objects.filter(email=attrs['email'], cliente=attrs['client_id']).first()

        if user and user.check_password(attrs['password']):
            return True
        raise serializers.ValidationError("Credenciales inválidas")
