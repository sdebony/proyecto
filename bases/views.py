from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin,\
     PermissionRequiredMixin
from django.views import generic

from django.contrib import messages
from datetime import date

from django.db.models import Sum


from .models import Idioma,Frase
from fac.models import FacturaEnc, AlquilerTubos,Tubos


class MixinFormInvalid:
    def form_invalid(self,form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin, MixinFormInvalid):
    login_url = 'bases:login'
    raise_exception=False
    redirect_field_name="redirecto_to"

    def handle_no_permission(self):
        from django.contrib.auth.models import AnonymousUser
        if not self.request.user==AnonymousUser():
            self.login_url='bases:sin_privilegios'
        return HttpResponseRedirect(reverse_lazy(self.login_url))


class Home(LoginRequiredMixin, generic.TemplateView):
    template_name = 'bases/home.html'
    login_url='bases:login'
    
      


class HomeSinPrivilegios(LoginRequiredMixin, generic.TemplateView):
    login_url = "bases:login"
    template_name="bases/sin_privilegios.html"


class IdiomaList(generic.ListView):
    template_name = "bases/idiomas.html"
    model = Idioma
    context_object_name="obj"



class FraseList(generic.ListView):
    template_name = "bases/frases.html"
    model = Frase
    context_object_name="obj"

    def get_queryset(self):
        qs = Frase.objects.all()
        idioma_id = self.request.GET.get("lang")
        if idioma_id:
            qs = qs.filter(idioma__id=idioma_id)
        return qs



def dashboard(request,id=None):
    template_name = "bases/cards.html"
#   clientes = Cliente.objects.filter(estado=True)
    
    contexto={}

    if request.method == "GET":
        #enc = FacturaEnc.objects.filter().all()
        enc = FacturaEnc.objects.filter(estado_factura='Creada').all()
        
        #Monto pendiente de facturar
        total=FacturaEnc.objects.filter(estado_factura='Creada').aggregate(Sum('total'))

        #Cantidad pedidos pendiente de entregar
        cant_fact=FacturaEnc.objects.filter(estado_factura='Creada').count
        
        #Tubos en alquiler
        cant_alq=AlquilerTubos.objects.filter(fecha_retiro__isnull=True).count()

        #total_tubos
        total_tubos=Tubos.objects.filter(estado=True).count()

       

               
        print("Alquileres")
        print(total_tubos)
        print(cant_alq)
       

        card1 = total["total__sum"]
        card2 = cant_fact
        card3 = cant_alq 
        card4= total_tubos 

        totales = {
            
            'card1':card1,  #Monto Total de pedidos pendientes de cobrar
            'card2':card2,  #Cantidad total de pedidos pendientes de cobrar
            'card3':card3,  #Cantidad de tubos en alquiler
            'card4':card4,  #% Total Tubos activos
            'card5':"40" #enc.total
        }
                
        
        print(card1)
        print(card2)
        
        contexto = {"tot":totales,"enc":enc}
        return render(request,template_name,contexto)
    
 
    return render(request,template_name,contexto)
