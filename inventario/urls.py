from django.urls import path
from .Views.ConvertUnitsAPIView.view import ConvertUnitsAPIView
from .Views.Cantidades.view import CantidadesView
from .Views.StockAPIView.view import StockAPIView
from .Views.ListarProductos.view import ListarProductos
from .Views.VenderProducto.view import VenderProducto
urlpatterns = [
    path('convert_units', ConvertUnitsAPIView.as_view(), name='convert_units'),
    path('Cantidades/', CantidadesView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy'
    }), name='cantidades'),
    path('Inventario/<operation>/', StockAPIView.as_view(), name='inventario'),

    path('ListarProductos/', ListarProductos.as_view(), name='listar_productos'),

    path('VenderProducto/', VenderProducto.as_view(), name='vender_producto'),
]