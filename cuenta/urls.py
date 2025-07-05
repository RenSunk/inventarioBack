from django.urls import path
from .views import *
from cuenta.Views.Perfil.view import Perfil
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('perfil/', Perfil.as_view(), name='perfil'),
]