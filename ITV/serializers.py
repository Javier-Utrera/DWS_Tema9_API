from datetime import date
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


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Vehiculo
        fields = '__all__'
        
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
        
class TrabajadorSerializer(serializers.ModelSerializer):
    trabajador_Vehiculo=VehiculoSerializer(many=True)
    trabajador_Inspeccion=InspeccionSerializer(many=True)
    estacion=EstacionItvSerializer(many=True)
    class Meta:
        model = Trabajador
        fields= '__all__'
        
class CitaSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields =['cliente','estacion','matricula','fecha_matriculacion',
                 'numero_bastidor','tipo_inspeccion','remolque','tipo_pago',
                 'fecha_propuesta','hora_propuesta']
        
        def validate_matricula(self,matricula):
            if len(matricula) > 7:
                raise serializers.ValidationError('La matrícula no puede tener más de 7 caracteres.')
            return matricula
        
        def validate_fecha_propuesta(self,fecha_propuesta):
            fechaHoy = date.today()
            if fecha_propuesta<fechaHoy:
                raise serializers.ValidationError('La fecha seleccionada')
            return fecha_propuesta   
        def validate_estacion(self,estacion):
            if len (estacion)<1:
                raise serializers.ValidationError('Seleccione al menos una estacion')
            return estacion
        
        def create(self,validated_data):
            cita=Cita.objects.create(
                cliente=validated_data['cliente'],
                estacion=validated_data['estacion'],
                matricula=validated_data['matricula'],
                numero_bastidor=validated_data['numero_bastidor'],
                tipo_inspeccion=validated_data['tipo_inspeccion'],
                remolque=validated_data['remolque'],
                tipo_pago=validated_data['tipo_pago'],
                fecha_matriculacion=validated_data['fecha_matriculacion'],
                fecha_propuesta=validated_data['fecha_propuesta'],
                hora_propuesta=validated_data['hora_propuesta']
            )
    
    