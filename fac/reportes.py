from django.shortcuts import render
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.utils import timezone

from datetime import date
from datetime import datetime

#import pandas as pd
#from pandas.io.json import json_normalize



from .models import FacturaEnc,FacturaDet, Cliente, Producto, AlquilerTubos

def imprimir_factura_recibo(request,id):
    template_name="fac/factura_one.html"

    enc = FacturaEnc.objects.get(id=id)
    det = FacturaDet.objects.filter(factura=id)

    context={
        'request':request,
        'enc':enc,
        'detalle':det
    }

    return render(request,template_name,context)

def imprimir_factura_list(request,f1,f2):
    template_name="fac/facturas_print_all.html"

    f1=parse_date(f1)
    f2=parse_date(f2)
    f2=f2 + timedelta(days=1)

    enc = FacturaEnc.objects.filter(fecha__gte=f1,fecha__lt=f2)
    f2=f2 - timedelta(days=1)
    
    context = {
        'request':request,
        'f1':f1,
        'f2':f2,
        'enc':enc
    }

    return render(request,template_name,context)

def imprimir_remito(request,id):
    template_name="fac/remito.html"

    enc = FacturaEnc.objects.get(id=id)
    det = FacturaDet.objects.filter(factura=id)
    cli = Cliente.objects.get(id=enc.cliente.id)
    prod= Producto.objects.all()

    datos = {
        'nro_remito':str(enc.id).zfill(6),
        'nro_cuenta':'0000001',
        'nro_factura':'',
        'nro_pedido':str(enc.id).zfill(6),
        'nro_orden':''
    
    }

   
    context={
        'request':request,
        'enc':enc,
        'det':det,
        'cli':cli,
        'datos':datos,
        'prod':prod
        
    }

    return render(request,template_name,context)

def reporte_alquileres(request):
    
    template_name="fac/alquileres_print.html"
    today = date.today()
    

    ultimoDiaMes=date.today().replace(day=1)+timedelta(days=-1)
    primerDiaMes=ultimoDiaMes.replace(day=1) #-timedelta(days=)
    
   

    titulo  = "Reporte de alquileres desde " + primerDiaMes.strftime('%Y/%m/%d') + " hasta el " + ultimoDiaMes.strftime('%Y/%m/%d')
    print(primerDiaMes)
    print(ultimoDiaMes)
    
    alq = AlquilerTubos.objects.filter(fecha_entrega__gte=primerDiaMes, fecha_entrega__lte=ultimoDiaMes).all().order_by('fecha_entrega')  



#    dfalq = pd.DataFrame(alq.values('cliente','fecha_entrega','fecha_retiro','codigo','descripcion','codigo_barra','fecha_venc'))
#    dfalq['fecha_entrega'] = pd.to_datetime(dfalq['fecha_entrega'],format="%Y/%m/%d")
#    dfalq['fecha_actual'] = pd.to_datetime(today,format="%Y/%m/%d")
#    if dfalq['fecha_retiro'].empty==False:
#        dfalq['fecha_retiro'] = pd.to_datetime(dfalq['fecha_retiro'],format="%Y/%m/%d")
#        dfalq["dias"] = (dfalq["fecha_retiro"] - dfalq["fecha_entrega"]).dt.days
#    else:
#        dfalq['fecha_retiro'] = pd.to_datetime(dfalq['fecha_retiro'],format="%Y/%m/%d")   
#        dfalq["dias"] = (today - dfalq["fecha_entrega"]).dt.days
#    json = asd.to_json(orient="records")  
#    print("*************")
#    print("**************")
#    print(dfalq)
    
    
    context = {
        'request':request,
        'today':today,
        'titulo':titulo,
        'alq':alq
    
    }

    return render(request,template_name,context)