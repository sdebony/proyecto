from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import ProductoSerializer,ClienteSerializer,TubosSerializer,FacturaSerializer
from inv.models import Producto, Tubos
from fac.models import Cliente, FacturaEnc

from django.db.models import Q

class ProductoList(APIView):
    
    def get(self,request):
        print("Productos API List")
        prod = Producto.objects.all()
        data = ProductoSerializer(prod,many=True).data
        return Response(data)

class ProductoDetalle(APIView):
    def get(self,request, codigo):
        prod = get_object_or_404(Producto,Q(codigo=codigo)|Q(codigo_barra=codigo))
        data = ProductoSerializer(prod).data
        return Response(data)

class ClienteList(APIView):

    print("Cliente Api List")
    def get(self,request):
        obj = Cliente.objects.all()
        data = ClienteSerializer(obj,many=True).data
        return Response(data)

class TubosList(APIView):

    print("Tubos Api List")
    def get(self,request):
        obj = Tubos.objects.all()
        data = TubosSerializer(obj,many=True).data
        return Response(data)

class TuboDetalle(APIView):
   
    def get(self,request, codigo):
        tub = get_object_or_404(Tubos,Q(codigo=codigo))
        data = TubosSerializer(tub).data
        return Response(data)

class PedidoList(APIView):
   
    def get(self,request):
        print("Productos API List")
        enc = FacturaEnc.objects.all()
        data = FacturaSerializer(enc,many=True).data
        return Response(data)

class PedidoDetalle(APIView):
   
    def get(self,request, codigo):
        enc = get_object_or_404(FacturaEnc,Q(id=codigo))
        data = FacturaSerializer(enc).data
        return Response(data)

      
   
     
     