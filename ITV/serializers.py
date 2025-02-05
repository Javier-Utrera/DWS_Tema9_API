from rest_framework import serializers
from .models import *

class TrabajadorSoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields= '__all__'
        
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'

#
class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vehiculo
        fields = '__all__'
#        
class InspeccionSerializer(serializers.ModelSerializer):
    trabajador=TrabajadorSoloSerializer()
    inspeccion_Factura=FacturaSerializer()
    vehiculo= VehiculoSerializer()
    class Meta:
        model = Inspeccion
        fields = '__all__'    
           
class EstacionItvSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacionItv
        fields = '__all__' 

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente 
        fields = '__all__' 
#
class CitaSerializer(serializers.ModelSerializer):
    estacion = EstacionItvSerializer() 
    cliente = ClienteSerializer()
    class Meta:
        model = Cita
        fields = '__all__'
        
class ClienteSerializerCompleto(serializers.ModelSerializer):
    cliente_cita = CitaSerializer(many=True) 
    class Meta:
        model = Cliente 
        fields = '__all__' 
#        
class TrabajadorSerializer(serializers.ModelSerializer):
    trabajador_Vehiculo=VehiculoSerializer(many=True)
    trabajador_Inspeccion=InspeccionSerializer(many=True)
    estacion=EstacionItvSerializer(many=True)
    class Meta:
        model = Trabajador
        fields= '__all__'