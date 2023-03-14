from rest_framework import serializers

from inv.models import Producto, Tubos
from fac.models import Cliente,FacturaEnc

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Producto
        fields='__all__'


class ClienteSerializer(serializers.ModelSerializer):

    class Meta:
        model=Cliente
        fields='__all__'


class TubosSerializer(serializers.ModelSerializer):

    class Meta:
        model=Tubos
        fields='__all__'

class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model=FacturaEnc
        fields='__all__'