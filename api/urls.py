from django.urls import path, include
from .views import ProductoList, ProductoDetalle, \
    ClienteList,TubosList,PedidoList,PedidoDetalle,TuboDetalle

urlpatterns = [
    path('v1/pedidos/',PedidoList.as_view(),name='pedido_list'),
    path('v1/pedidos/<str:codigo>',PedidoDetalle.as_view(),name='pedido_detalle'),
    path('v1/productos/',ProductoList.as_view(),name='producto_list'),
    path('v1/productos/<str:codigo>',ProductoDetalle.as_view(),name='producto_detalle'),
    path('v1/clientes/',ClienteList.as_view(),name='cliente_list'),
    path('v1/tubos/',TubosList.as_view(),name='tubos_list'),
    path('v1/tubos/<str:codigo>',TuboDetalle.as_view(),name='tubos_detalle'),
    
    
]