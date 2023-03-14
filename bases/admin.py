from django.contrib import admin

# Register your models here.

from  bases.models import Frase,Idioma

from inv.models import Producto,Categoria,SubCategoria,Marca,UnidadMedida,Tubos

from cmp.models import Proveedor,ComprasEnc,ComprasDet

from fac.models import FacturaEnc,FacturaDet,Cliente,AlquilerTubos, LiquidacionEnc,LiquidacionDet


#Modelo Base
admin.site.register(Frase)
admin.site.register(Idioma)

#Modelo Inv (Inventario)
admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Marca)
admin.site.register(UnidadMedida)

#Modelo cmp (Compras)
admin.site.register(Proveedor)
admin.site.register(ComprasEnc)
admin.site.register(ComprasDet)

#Modelo fac (Facturas)
admin.site.register(FacturaEnc)
admin.site.register(FacturaDet)
admin.site.register(Cliente)

#Modelo Inv (Tubos)
admin.site.register(Tubos)
admin.site.register(AlquilerTubos)


#Modelo fac (Liquidaciones)
admin.site.register(LiquidacionEnc)
admin.site.register(LiquidacionDet)
