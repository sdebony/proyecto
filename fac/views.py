from django.shortcuts import render,redirect
from django.views import generic

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages

from datetime import date
from datetime import datetime
from datetime import timedelta

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Cliente, FacturaEnc, FacturaDet, AlquilerTubos, LiquidacionEnc,LiquidacionDet
from .forms import ClienteForm,AlquilerForm,LiquidacionEncForm
import inv.views as inv
from inv.models import Producto, Tubos


class ClienteView(SinPrivilegios, generic.ListView):
    model = Cliente
    template_name = "fac/cliente_list.html"
    context_object_name = "obj"
    permission_required="cmp.view_cliente"

class LiquidacionView(SinPrivilegios, generic.ListView):
    model = LiquidacionEnc
    template_name = "fac/liquidacion_list.html"
    context_object_name = "obj"
    permission_required="fac.view_liquidacion"


class VistaBaseCreate(SuccessMessageMixin,SinPrivilegios, \
    generic.CreateView):
    context_object_name = 'obj'
    success_message="Registro Agregado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.uc = self.request.user
        return super().form_valid(form)

class VistaBaseEdit(SuccessMessageMixin,SinPrivilegios, \
    generic.UpdateView):
    context_object_name = 'obj'
    success_message="Registro Actualizado Satisfactoriamente"

    def form_valid(self, form):
        form.instance.um = self.request.user.id
        return super().form_valid(form)

class ClienteNew(VistaBaseCreate):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.add_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get")
        
        try:
            t = request.GET["t"]
        except:
            t = None

        print(t)
        
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form, 't':t})

class ClienteEdit(VistaBaseEdit):
    model=Cliente
    template_name="fac/cliente_form.html"
    form_class=ClienteForm
    success_url= reverse_lazy("fac:cliente_list")
    permission_required="fac.change_cliente"

    def get(self, request, *args, **kwargs):
        print("sobre escribir get en editar")

        print(request)
        
        try:
            t = request.GET["t"]
        except:
            t = None

        
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        print(form_class,form,context)
        return self.render_to_response(context)

class AlquilerTubosEdit(VistaBaseEdit):
    model=AlquilerTubos
    template_name="fac/alquiler_form.html"
    form_class=AlquilerForm
    success_url= reverse_lazy("fac:alquileres_list")
    permission_required="fac.view_alquilerc"

    
    def get(self, request, *args, **kwargs):
        print("Editar AsignaTubos << AlquilerTubosEdit >>")
       
        print(request)
        try:
            t = request.GET["t"]
        except:
            t = None

        

        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form,t=t)
        return self.render_to_response(context)

@login_required(login_url="/login/")

@permission_required("fac.change_cliente",login_url="/login/")

def clienteInactivar(request,id):
    cliente = Cliente.objects.filter(pk=id).first()

    if request.method=="POST":
        if cliente:
            cliente.estado = not cliente.estado
            cliente.save()
            return HttpResponse("OK")
        return HttpResponse("FAIL")
    
    return HttpResponse("FAIL")

class FacturaView(SinPrivilegios, generic.ListView):
    model = FacturaEnc
    template_name = "fac/factura_list.html"
    context_object_name = "obj"
    permission_required="fac.view_facturaenc"

    def get_queryset(self):
        user = self.request.user
        # print(user,"usuario")
        qs = super().get_queryset()
        for q in qs:
            print(q.uc,q.id)
        
        if not user.is_superuser:
            qs = qs.filter(uc=user)

        for q in qs:
            print(q.uc,q.id)

        return qs

@login_required(login_url='/login/')
@permission_required('fac.change_facturaenc', login_url='bases:sin_privilegios')
def facturas(request,id=None):

    template_name='fac/facturas.html' 
    clientes = Cliente.objects.filter(estado=True)
    
    detalle = {} 
    contexto={}

    if request.method == "GET":
        enc = FacturaEnc.objects.filter(pk=id).first()
        if id:
            if not enc:
                messages.error(request,'Factura No Existe')
                return redirect("fac:factura_list")

            usr = request.user
            if not usr.is_superuser:
                if enc.uc != usr:
                    messages.error(request,'Factura no fue creada por usuario')
                    return redirect("fac:factura_list")

        if not enc:
            encabezado = {
                'id':0,
                'fecha':datetime.today(),
                'cliente':0,
                'sub_total':0.00,
                'descuento':0.00,
                'total': 0.00
            }
            detalle=None
        else:
            
            encabezado = {
                'id':enc.id,
                'fecha':enc.fecha,
                'fecha_entrega':enc.fecha_entrega,
                'cliente':enc.cliente,
                'sub_total':enc.sub_total,
                'descuento':enc.descuento,
                'total':enc.total,
                'estado_factura':enc.estado_factura
            }
        
            detalle=FacturaDet.objects.filter(factura=enc.id)



        contexto = {"enc":encabezado,"det":detalle,"clientes":clientes}
        return render(request,template_name,contexto)
    
    if request.method == "POST":

        cliente = request.POST.get("enc_cliente")
        fecha  = request.POST.get("fecha")
        fecha_entrega  = request.POST.get("fecha_entrega")
       
       
        if not fecha_entrega:
            messages.error(request,'No pudo detectar fecha de entrega')
            return redirect("fac:factura_list")

        if not cliente:
            messages.error(request,'No pudo detectar el cliente')
            return redirect("fac:factura_list")

        cli=Cliente.objects.get(pk=cliente)
        
        if not id:
            enc = FacturaEnc(
                cliente = cli,
                fecha = fecha,
                fecha_entrega = fecha_entrega
            )
            if enc:
                enc.save()
                id = enc.id
        else:
            enc = FacturaEnc.objects.filter(pk=id).first()
            if enc:
                enc.uc = request.user
                enc.cliente = cli
                enc.fecha_entrega = fecha_entrega
                enc.save()

        if not id:
            messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
            return redirect("fac:factura_list")
        

        codigo = request.POST.get("codigo")
        descripcion = request.POST.get("descripcion")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        s_total = request.POST.get("sub_total_detalle")
        descuento = request.POST.get("descuento_detalle")
        total = request.POST.get("total_detalle")
        #estado_factura = request.POST.get("estado_factura")

                
        if codigo:

            if not precio:
                messages.error(request,'Producto sin precio')
                return redirect("fac:factura_edit",id=id)

            #valido que exista un producto y el cliente
            if not cantidad:
            
                messages.error(request,'Ingrese la cantidad')
                return redirect("fac:factura_edit",id=id)

    

            prod = Producto.objects.get(codigo=codigo)
            

            descripcion= prod.descripcion
            det = FacturaDet(
                factura = enc,
                codigo = prod,
                descripcion = descripcion,
                cantidad = cantidad,
                precio = precio,
                sub_total = s_total,
                descuento = descuento,
                total = total
            )
        
            if det:
                det.save()

        return redirect("fac:factura_edit",id=id)

    return render(request,template_name,contexto)


class ProductoView(inv.ProductoView):
    template_name="fac/buscar_producto.html" 


class AlquileresView(SinPrivilegios, generic.ListView):

    model = AlquilerTubos
    template_name="fac/alquileres_list.html" 
    context_object_name = "obj"
    permission_required="fac.sup_caja_facturadet"


def liquidarAlquiler(request,id=None):

    template_name = "fac/liquidacion_form.html"
    liqEnc={}
    liqDet={}
    alq={}
    contexto={}


    if request.POST.get("fecha_desde"):
        ultimoDiaMes=datetime.strptime(request.POST.get("fecha_hasta"), "%Y-%m-%d")
        primerDiaMes=datetime.strptime(request.POST.get("fecha_desde"), "%Y-%m-%d")
    else:
        print("tomo mes anterior - ")
        ultimoDiaMes=datetime.today().replace(day=1)+timedelta(days=-1)
        primerDiaMes=ultimoDiaMes.replace(day=1) 
    #alq = AlquilerTubos.objects.filter(fecha_entrega__gte=primerDiaMes, fecha_entrega__lte=ultimoDiaMes).all().order_by('fecha_entrega')


    print("LiquidarAlquiler")
    print(primerDiaMes)
    print(ultimoDiaMes) 
   
    
    if request.method == "GET":
    
        print("get")
        print(id)
        liqEnc = LiquidacionEnc.objects.filter(id=id).first()
    
        if liqEnc:       
            print("idLiqEnc")
            print(liqEnc.id)
            liqDet = LiquidacionDet.objects.filter(idliqenc=id)
            if not liqDet: #Tiene detalle
                print("3")
                liqDet = None     
        else:
            today = date.today()
            liqEnc = {
                'fecha':today,
                'mes': ultimoDiaMes.month,
                'fecha_desde':primerDiaMes,
                'fecha_hasta':ultimoDiaMes,
                'realizada':0

            }
        print(liqEnc)
        print(liqDet)
        print(alq)
    
        contexto={"liqEnc":liqEnc,"liqDet":liqDet,"alq":alq}
        return render(request, template_name, contexto)

    if request.method == "POST":
        
        print("post")
        liqEnc = LiquidacionEnc.objects.filter(pk=id).first()
        if not liqEnc:
            #Actualizo encabezado
            print("1")
            fecha_new = datetime.strptime(request.POST.get("fecha_desde"), "%Y-%m-%d")
            int_mes = request.POST.get("mes") #fecha_new.month 
            usr = request.user
           
            liqEnc = LiquidacionEnc(
                uc=usr,
                fecha = datetime.strptime(request.POST.get("fecha"), "%Y-%m-%d"),
                mes  = int_mes,
                fecha_desde  = request.POST.get("fecha_desde"),
                fecha_hasta = request.POST.get("fecha_hasta"),
                realizada = 0
            )
            print("2")
            liqEnc.save()
            idliqEnc = liqEnc.id

            liqDet = LiquidacionDet.objects.filter(idliqenc=liqEnc.id)  ##Todos los alquileres guardados para ese encabezado  
            if  liqDet:
                print("3")
                #Actualizo detalle y estado
                cli = Cliente.objects.filter(id=alq.cliente).fisrt()
                tub = Tubos.objects.filter(codigo=alq.codigo)
                liqDet = {
                    'idliqenc':idliqEnc,
                    'fecha_desde':primerDiaMes,
                    'fecha_hasta':ultimoDiaMes,
                    'dias':0,
                    'cliente':cli.id,
                    'codigo_tubo':tub.codigo
                }
                print("4")
                liqDet.save()
                print(liqDet.id)
            else:
            #copio lo pendiente de alquileres
                print(primerDiaMes)
                print(ultimoDiaMes)
                alq = AlquilerTubos.objects.filter(fecha_entrega__gte=primerDiaMes, fecha_entrega__lte=ultimoDiaMes).all().order_by('fecha_entrega')
                print("5")
                if alq:
                    for obj in alq:
                        print("***********alq to det**************")
                        print(obj.cliente)
                        print(liqEnc.id)
                        cliente = obj.cliente.id
                        cli=Cliente.objects.get(pk=cliente)
                        codtubo = obj.codigo
                        print(codtubo)
                       
                        tub = Tubos.objects.get(codigo=codtubo)
                        alqItem = AlquilerTubos.objects.get(pk=obj.id)

                        #Traigo las fechas de cálculo del queryset
                        fecha_hasta = obj.fecha_retiro
                        fecha_desde  = obj.fecha_entrega
                        print("fecha_desde")
                        print(fecha_desde)
                        print("fecha hasta")
                        print(fecha_hasta)
                        if fecha_desde < primerDiaMes.date():
                            fecha_desde = primerDiaMes.date()
                        if fecha_hasta==None:
                            fecha_hasta = ultimoDiaMes.date()
                        
                        print("2.fecha_desde")
                        print(fecha_desde)
                        print("2.fecha hasta")
                        print(fecha_hasta)
                        dias = (fecha_hasta-fecha_desde).days
                        print("dias")
                        print(dias)
                        
                        if not fecha_hasta:
                            fecha_hasta = ultimoDiaMes
                        if fecha_hasta >ultimoDiaMes.date():
                            fecha_hasta = ultimoDiaMes
                        liqDet = LiquidacionDet(
                            idliqenc=liqEnc,
                            idalq=alqItem,
                            fc=datetime.today(),
                            uc=usr,
                            fecha_desde=obj.fecha_entrega,
                            fecha_hasta=fecha_hasta,
                            dias = dias, 
                            cliente =cli,
                            codigo_tubo = tub
                                    
                        ) ##Todos los alquileres del periodo  
                        liqDet.save()

                    return redirect("fac:liquidacion_list")
        return redirect("fac:liquidacion_list")


    contexto={"liqEnc":liqEnc,"liqDet":liqDet,"alq":alq}
    return render(request, template_name, contexto)


def registrar_alquiler(request,id=None,idpedido=None):
    template_name = "fac/alquiler_form.html"

    #1 Validar que exista una factura con ese id
    #2 Si existe tomar. validar que existe en Alquileres ese id
    #3 Si existe en Alquileres, tomar esa informacion
    #4 Si no existe en Alquileres, tomar la info de Facturas y grabar alquileres
    #5 Editar registro Alquileres

    enc = {}
    alq= {}
    tub = {}
    cli={}
    alq_todos= None
    contexto={}

            

    if request.method == "GET":
        print("Get --> ") 
        print(id) 
        print(idpedido)

        cli = Cliente.objects.filter(estado=True)
        alq = AlquilerTubos.objects.filter(id=id).first()  ## El registro seleccionado
            
        if alq:       
            print("1")
           
            
            enc = FacturaEnc.objects.get(pk=idpedido)
            alq_todos = AlquilerTubos.objects.filter(idpedido=enc.id)  ##Todos los registros del pedido  
            cliente = enc.cliente.id
            cli=Cliente.objects.filter(pk=cliente)
            if id:
                print("2")
                if not enc:
                    print("3")
                    messages.error(request,'Factura No Existe')
                    return redirect("fac:factura_list")
            else:
                print("4")
                alq = None
        #else:
        #    return redirect("fac:alquileres_list")
            
        print("5")
        print(alq)
        contexto={"alq":alq,"cli":cli,"alq_todos":alq_todos,"enc":enc}
        return render(request, template_name, contexto)

    if request.method == "POST":
        
            print("post")
            idpedido  = request.POST.get("idpedido")
            cliente = request.POST.get("enc_cliente")
            fecha_entrega  = request.POST.get("fecha_entrega")
            fecha_retiro = request.POST.get("fecha_retiro")
            codigo  = request.POST.get("codigo")
            descripcion  = request.POST.get("descripcion")
            codigo_barra  = request.POST.get("codigo_barra")
            fecha_venc = request.POST.get("fecha_venc")
           
            print(id)
            if not idpedido.isnumeric():
                messages.error(request,'Nro de pedido incorrecto')
                return redirect("fac:alquileres_new")

            if not idpedido:
                messages.error(request,'No Puedo encontrar el pedido')
                return redirect("fac:alquileres_new")


            enc = FacturaEnc.objects.filter(pk=idpedido).first()
            if enc:
                cliente = enc.cliente.id
                cli=Cliente.objects.filter(pk=cliente)
                alq_todos = AlquilerTubos.objects.filter(idpedido=enc.id)  ##Todos los registros del pedido  
            else:
                messages.error(request,'No Puedo encontrar el pedido')
                return redirect("fac:alquileres_new")


            if codigo:
                if not fecha_retiro:  #Si no retira osea es vacio este campo, solo tubos no alquilados
                    tub = Tubos.objects.filter(codigo=codigo, estado=True)
                    if not tub:
                            if not id:
                                messages.error(request,'Tubo inexistente o inactivo')
                                return redirect("fac:alquileres_new")
                    
                else:
                    tub = Tubos.objects.filter(codigo=codigo)
                    if not tub:
                        messages.error(request,'Tubo inexistente')
                        return redirect("fac:alquileres_new")
                
            
            if not id:
                print("12")
                if codigo:
                    print("12-a")
                    print(codigo)
                    tub = Tubos.objects.get(codigo=codigo)
                    if tub:
                        cli=Cliente.objects.filter(pk=cliente)
                        descripcion = tub.descripcion
                        codigo_barra = tub.codigo_barra
                        fecha_venc = tub.fecha_venc
                        usr = request.user
                        if not fecha_retiro:
                            fecha_retiro = None
                            print("12-b")
                            tub.estado=False
                            tub.save()
                        else:
                           
                            print("12-b1")
                            tub.estado=True
                            tub.save()
                            
                        if fecha_entrega:
                            cli=Cliente.objects.get(pk=cliente)
                            alq = AlquilerTubos (
                                uc=usr,
                                idpedido=enc,
                                fecha=datetime.today(),
                                fecha_entrega=fecha_entrega,
                                fecha_retiro = fecha_retiro,
                                cliente= cli,
                                codigo=tub,
                                descripcion=descripcion,
                                codigo_barra=codigo_barra,
                                fecha_venc=fecha_venc
                                )
                            if alq:
                                print("12-c")
                                alq.save()
                                id = alq.id

                          
                        else:  #ELSE FECHA ENTREGA
                            print("fecha entrega vacía")
                            print(fecha_entrega)
                            alq = {
                                'id':0,
                                'idpedido':idpedido,
                                'fecha':datetime.today(),
                                'cliente':cli,
                                'codigo':codigo,
                                'descripcion':descripcion,
                                'codigo_barra':codigo_barra,
                                'fecha_venc':fecha_venc
                            }
                    else:
                        print("Tubo inexistente o inactivado")
                        messages.error(request,'Tubo inexistente o inactivado')
                        return redirect("fac:alquileres_new")
                else:
                    alq = {
                        'id':0,
                        'idpedido':idpedido,
                        'fecha':datetime.today(),
                        'fecha_entrega':fecha_entrega,
                        'cliente':cli
                    }
                

            else:
                print("3")
                alq = AlquilerTubos.objects.filter (id=id).first()
                tub = Tubos()
                tub = Tubos.objects.get(codigo=codigo)
                if tub:
                    print("tubos")
                    descripcion = tub.descripcion
                    codigo_barra = tub.codigo_barra
                    fecha_venc = tub.fecha_venc
               
                enc = FacturaEnc()
                cli = Cliente()
                cli=Cliente.objects.get(pk=cliente)
                enc = FacturaEnc.objects.get(pk=idpedido)
                if enc:
                    print("enc-->OK")
                    print(fecha_entrega)
                    print(fecha_retiro)
                    if not fecha_retiro:
                        fecha_retiro = None
                    usr = request.user
                    alq = AlquilerTubos(
                            id=id,
                            fc=datetime.today(),
                            uc=usr,
                            idpedido=FacturaEnc.objects.get(pk=idpedido),
                            fecha=datetime.today(),
                            cliente=Cliente.objects.get(pk=cliente),
                            fecha_entrega=fecha_entrega,
                            fecha_retiro = fecha_retiro,
                            codigo= tub,
                            descripcion=descripcion,
                            codigo_barra=codigo_barra,
                            fecha_venc=fecha_venc
                    )
                    if alq:
                            print("save")
                            alq.save()
                            if not fecha_retiro:
                                fecha_retiro = None
                                print("22 --> Bloqueo Tubo")
                                tub.estado=False
                                tub.save()
                            else:
                            
                                print("22-> OK")
                                tub.estado=True
                                tub.save()

                        
            if not idpedido:
                print("5")
                messages.error(request,'No Puedo Continuar No Pude Detectar No. de Factura')
                return redirect("fac:alquileres_list")
            
            if id:
                print("6")
                print("new id")
                print(id)
                return redirect("fac:alquileres_list")
#                return redirect("fac:alquileres_edit", id=id,idpedido=idpedido)

   
    contexto={"alq":alq,"cli":cli,"alq_todos":alq_todos,"enc":enc}
    return render(request,template_name,contexto)
    
def borrar_detalle_factura(request, id):
    template_name = "fac/factura_borrar_detalle.html"

    det = FacturaDet.objects.get(pk=id)

    if request.method=="GET":
        context={"det":det}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            det.id = None
            det.cantidad = (-1 * det.cantidad)
            det.sub_total = (-1 * det.sub_total)
            det.descuento = (-1 * det.descuento)
            det.total = (-1 * det.total)
            det.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)


def pagar_factura(request, id):
    template_name = "fac/factura_pagar.html"

    enc = FacturaEnc.objects.get(pk=id)

    if request.method=="GET":
        context={"enc":enc}

    if request.method == "POST":
        usr = request.POST.get("usuario")
        pas = request.POST.get("pass")

        user =authenticate(username=usr,password=pas)

        if not user:
            return HttpResponse("Usuario o Clave Incorrecta")
        
        if not user.is_active:
            return HttpResponse("Usuario Inactivo")

        if enc.estado_factura !="Creada":
            return HttpResponse("No se puede realizar el pago. Estado:" + enc.estado_factura)

        if user.is_superuser or user.has_perm("fac.sup_caja_facturadet"):
            enc.estado_factura="Cobrada" 
            enc.save()

            return HttpResponse("ok")

        return HttpResponse("Usuario no autorizado")
    
    return render(request,template_name,context)


@login_required(login_url="/login/")
@permission_required("fac.change_cliente",login_url="/login/")
def cliente_add_modify(request,pk=None):
    template_name="fac/cliente_form.html"
    context = {}

    if request.method=="GET":
        context["t"]="fc"
        if not pk:
            form = ClienteForm()
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            form = ClienteForm(instance=cliente)
            context["obj"]=cliente
        context["form"] = form
    else:
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        celular = request.POST.get("celular")
        tipo = request.POST.get("tipo")
        usr = request.user

        if not pk:
            cliente = Cliente.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                celular = celular,
                tipo = tipo,
                uc=usr,
            )
        else:
            cliente = Cliente.objects.filter(id=pk).first()
            cliente.nombres=nombres
            cliente.apellidos=apellidos
            cliente.celular = celular
            cliente.tipo = tipo
            cliente.um=usr.id

        cliente.save()
        if not cliente:
            return HttpResponse("No pude Guardar/Crear Cliente")
        
        id = cliente.id
        return HttpResponse(id)
    
    return render(request,template_name,context)

    
class LiquidacionDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):

    permission_required="fac.delete_liquidacion"
    model=LiquidacionEnc
    template_name='fac/liquidacion_det.html'
    context_object_name='obj'
    success_url=reverse_lazy("fac:liquidacion_list")
    success_message="Liquidación Eliminada Satisfactoriamente"


class AlquilerDel(SuccessMessageMixin,SinPrivilegios, generic.DeleteView):

    permission_required="fac.delete_alquiler"
    model=AlquilerTubos
    template_name='fac/alquileres_del.html'
    context_object_name='obj'
    success_url=reverse_lazy("fac:alquileres_list")
    success_message="Liquidación Eliminada Satisfactoriamente"