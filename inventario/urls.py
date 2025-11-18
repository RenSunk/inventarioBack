from django.urls import path
from .Views.ConvertUnitsAPIView.view import ConvertUnitsAPIView
from .Views.Cantidades.view import CantidadesView

from .Views.ListarProductos.view import ListarProductos
from .Views.VenderProducto.view import VenderProducto
from .Views.AgregarProducto.view import AgregarProducto
from .Views.Producto.view import  ProductoView
from .Views.ProductoCantidad.view import ProductoCantidadView

urlpatterns = [
    path('convert_units', ConvertUnitsAPIView.as_view(), name='convert_units'),
    path('Cantidades/', CantidadesView.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'delete': 'destroy'
    }), name='cantidades'),
    path('ListarProductos/', ListarProductos.as_view(), name='listar_productos'),
    path('VenderProducto/', VenderProducto.as_view(), name='vender_producto'),
    path('AgregarProducto/', AgregarProducto.as_view(), name='agregar_producto'),
    path('Producto/<int:product_id>/', ProductoView.as_view(), name='modificar_producto'),
    path('ProductoCantidad/<int:product_unit_id>/', ProductoCantidadView.as_view(), name='producto_cantidad'),
    path('ProductoCantidad/', ProductoCantidadView.as_view(), name='agregar_cantidad'),
]