from django.urls import path, include

from .views import ClienteView,ClienteNew,ClienteEdit,clienteInactivar, \
    FacturaView, facturas, \
    ProductoView, AlquileresView,LiquidacionDel , AlquilerDel,\
    LiquidacionView, liquidarAlquiler, registrar_alquiler, \
    borrar_detalle_factura,cliente_add_modify,  pagar_factura

#LiquidacionView
    
from .reportes import imprimir_factura_recibo, imprimir_factura_list,imprimir_remito,reporte_alquileres

urlpatterns = [
    path('clientes/',ClienteView.as_view(), name="cliente_list"),
    path('clientes/new',ClienteNew.as_view(), name="cliente_new"),
    path('clientes/<int:pk>',ClienteEdit.as_view(), name="cliente_edit"),
    path('clientes/estado/<int:id>',clienteInactivar, name="cliente_inactivar"),

  
  
    path('facturas/',FacturaView.as_view(), name="factura_list"),
    path('facturas/new',facturas, name="factura_new"),
    path('facturas/edit/<int:id>',facturas, name="factura_edit"),
    
    
    path('facturas/buscar-producto',ProductoView.as_view(), name="factura_producto"),

    path('facturas/borrar-detalle/<int:id>',borrar_detalle_factura, name="factura_borrar_detalle"),
    path('facturas/pagar-factura/<int:id>',pagar_factura, name="factura_pagar"),

    path('facturas/imprimir/<int:id>',imprimir_factura_recibo, name="factura_imprimir_one"),
    path('facturas/imprimir/remito/<int:id>',imprimir_remito, name="imprimir_remito"),
    path('facturas/imprimir-todas/<str:f1>/<str:f2>',imprimir_factura_list, name="factura_imprimir_all"),

    path('facturas/clientes/new/',cliente_add_modify,name="fac_cliente_add"),
    path('facturas/clientes/<int:pk>',cliente_add_modify,name="fac_cliente_mod"),

    
    path('alquileres/',AlquileresView.as_view(), name="alquileres_list"),
    path('alquileres/new',registrar_alquiler, name="alquileres_new"),
    path('alquileres/edit/<int:id>/<int:idpedido>',registrar_alquiler, name="alquileres_edit"),
    path('alquileres/listado/', reporte_alquileres, name='alquileres_print_all'),
    path('alquileres/delete/<int:pk>',AlquilerDel.as_view(), name='alquileres_del'),

    path('liquidaciones/',LiquidacionView.as_view(), name="liquidacion_list"),
    path('liquidaciones/new/',liquidarAlquiler, name="liquidacion_new"),
    path('liquidaciones/edit/<int:id>',liquidarAlquiler, name="liquidacion_edit"),
    path('liquidaciones/delete/<int:pk>',LiquidacionDel.as_view(), name='liquidacion_del'),
   
    

]