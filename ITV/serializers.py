from rest_framework import serializers
from .models import *

class EstacionItvSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacionItv
        fields = '__all__' 

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'    

class CitaSerializer(serializers.ModelSerializer):
    
    cliente=ClienteSerializer()
    estacion=EstacionItvSerializer()
    
    
    class Meta:
        model = Cita
        fields = '__all__'