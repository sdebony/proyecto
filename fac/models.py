from django.db import models

#Para los signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

from bases.models import ClaseModelo, ClaseModelo2
from inv.models import Producto, Tubos



class Cliente(ClaseModelo):
    NAT='Natural'
    JUR='Jurídica'
    TIPO_CLIENTE = [
        (NAT,'Natural'),
        (JUR,'Jurídica')
    ]

    INS='Responsable Inscripto'
    N_INS='No Inscripto'
    EXT='Exento'
    CFIN = 'Consumidor Final'
    TIPO_IVA = [
        (INS,'Responsable Inscripto'),
        (N_INS,'No Inscripto'),
        (EXT,'Exento'),
        (CFIN, 'Consumidor Final')

    ]
    nombres = models.CharField(
        max_length=100
    )
    apellidos = models.CharField(
        max_length=100
    )
    direccion1 = models.CharField(
        max_length=100
    )
    direccion2 = models.CharField(
        max_length=100
    )
    direccion3 = models.CharField(
        max_length=100
    )
    tipo_iva=models.CharField(
        max_length=10,
        choices=TIPO_IVA,
        default=EXT
    )

    cuit = models.CharField(
        max_length=20,
        default=0
    )

    celular = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    tipo=models.CharField(
        max_length=10,
        choices=TIPO_CLIENTE,
        default=NAT
    )

    def __str__(self):
        return '{} {}'.format(self.apellidos,self.nombres)

    def save(self, *args, **kwargs):
        self.nombres = self.nombres.upper()
        self.apellidos = self.apellidos.upper()
        super(Cliente, self).save( *args, **kwargs)

    class Meta:
        verbose_name_plural = "Clientes"

class FacturaEnc(ClaseModelo2):

    CREADA='Creada'
    COBRADA='Cobrada'
    PEND_GENERACIÖN='Pend.  Fact Electrónica'
    GENERADA='Fact Electronica generada'
    PEND_ENVIO='Fact pend envio'
    ENVIADA='Fact enviada'
    CERRADA='Cerrada'
    ESTADO_FACTURA = [
        (CREADA,'Creada'),
        (COBRADA,'Cobrada'),
        (PEND_GENERACIÖN,'Pend.  Fact Electrónica'),
        (GENERADA,'Fact Electronica generada'),
        (PEND_ENVIO,'Fact pend envio'),
        (ENVIADA,'Fact enviada'),
        (CERRADA,'Cerrada')
    ]

    
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_entrega=models.DateField()
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    estado_factura=models.CharField(
        max_length=25,
        choices=ESTADO_FACTURA,
        default=CREADA
    )


    def __str__(self):
        return '{}'.format(self.id)

    def save(self):
        self.total = self.sub_total - self.descuento
        super(FacturaEnc,self).save()

    class Meta:
        verbose_name_plural = "Encabezado Facturas"
        verbose_name="Encabezado Factura"
        permissions = [
            ('sup_caja_facturaenc','Permisos de Supervisor de Caja Encabezado')
        ]

class FacturaDet(ClaseModelo2):
    factura = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    codigo=models.ForeignKey(Producto,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad=models.BigIntegerField(default=0)
    precio=models.FloatField(default=0)
    sub_total=models.FloatField(default=0)
    descuento=models.FloatField(default=0)
    total=models.FloatField(default=0)
    


    def __str__(self):
        return '{}'.format(self.factura) + ' - ' + '{}'.format(self.id)

    def save(self):
        
        self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
        self.total = self.sub_total - float(self.descuento)
        super(FacturaDet, self).save()
    
    class Meta:
        verbose_name_plural = "Detalles Facturas"
        verbose_name="Detalle Factura"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]

class AlquilerTubos(ClaseModelo):

    idpedido = models.ForeignKey(FacturaEnc,on_delete=models.CASCADE)
    fecha = models.DateField() #Fecha registración
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_entrega=models.DateField(null=True, blank=True)
    fecha_retiro=models.DateField(null=True, blank=True)
    codigo =models.ForeignKey(Tubos,on_delete=models.CASCADE,null=True,default='')
    descripcion = models.CharField(max_length=200,null=True,default='')
    codigo_barra = models.CharField(max_length=15,default='0') #Codigo de Barras del tubo
    fecha_venc=models.DateField(null=True, blank=True)

    def __str__(self):
       
        return '{}'.format(self.id) #+ ' - fac: ' + '{}'.format(self.idpedido) 

   
    class Meta:
        verbose_name_plural = "Alquileres Tubos"
        verbose_name="Alquiler de Tubos"
        permissions = [
            ('sup_caja_facturadet','Permisos de Supervisor de Caja Detalle')
        ]

class LiquidacionEnc(ClaseModelo):
     fecha = models.DateField() #Fecha registración
     mes = models.BigIntegerField()
     fecha_desde = models.DateField()
     fecha_hasta = models.DateField()
     realizada = models.BooleanField()

     def __str__(self):
        return '{}'.format(self.id)

     class Meta:
        verbose_name_plural = "Liquidaciones Encabezado"
        
class LiquidacionDet(ClaseModelo):
     idliqenc = models.ForeignKey(LiquidacionEnc, on_delete=models.CASCADE)
     idalq = models.ForeignKey(AlquilerTubos, on_delete=models.CASCADE)
     fecha_desde = models.DateField()
     fecha_hasta = models.DateField()
     dias = models.BigIntegerField()
     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
     codigo_tubo = models.ForeignKey(Tubos, on_delete=models.CASCADE)

     def __str__(self):
        return '{}'.format(self.id) + ' - Enc: ' + '{}'.format(self.idliqenc) + ' - Alq: ' + '{}'.format(self.idalq) 

     class Meta:
        verbose_name_plural = "Liquidaciones Detalle"

@receiver(post_save, sender=FacturaDet)

def detalle_fac_guardar(sender,instance,**kwargs):
    factura_id = instance.factura.id
    #producto_id = instance.producto.id
    producto_id = instance.codigo.id

    print("detalle_fac_guardar")
    print(producto_id)

    enc = FacturaEnc.objects.get(pk=factura_id)
    if enc:
        sub_total = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(sub_total=Sum('sub_total')) \
            .get('sub_total',0.00)
        
        descuento = FacturaDet.objects \
            .filter(factura=factura_id) \
            .aggregate(descuento=Sum('descuento')) \
            .get('descuento',0.00)
        
        enc.sub_total = sub_total
        enc.descuento = descuento
        enc.save()

    prod=Producto.objects.filter(pk=producto_id).first()
    if prod:
        cantidad = int(prod.existencia) - int(instance.cantidad)
        prod.existencia = cantidad
        prod.save()



