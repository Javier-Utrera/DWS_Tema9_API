from datetime import date
from rest_framework import serializers
from .models import *
from .forms import *
import re

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

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields= '__all__'   
             
class TrabajadorSerializer(serializers.ModelSerializer):
    usuario=UsuarioSerializer()
    trabajador_Vehiculo=VehiculoSerializer(many=True)
    trabajador_Inspeccion=InspeccionSerializer(many=True)
    estacion=EstacionItvSerializer(many=True)
    class Meta:
        model = Trabajador
        fields= '__all__'

class EstacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacionItv
        fields='__all__'

class LocalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = '__all__'


class TrabajadorResumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = '__all__'

class InspeccionResumenSerializer(serializers.ModelSerializer):
    trabajador = TrabajadorResumenSerializer()

    class Meta:
        model = Inspeccion
        fields = '__all__'

class VehiculoSerializerCompleto(serializers.ModelSerializer):

    propietario = ClienteSerializerCompleto()

    trabajadores = TrabajadorSoloSerializer(read_only=True, many=True)

    inspecciones = InspeccionSerializer(read_only=True, many=True, source='vehiculo_Inspeccion')

    fecha_matriculacion = serializers.DateField(format='%d-%m-%Y')

    tipo_vehiculo = serializers.CharField(source='get_tipo_vehiculo_display')
    combustible = serializers.CharField(source='get_combustible_display')

    class Meta:
        model = Vehiculo
        fields = (
            'id',
            'marca',
            'modelo',
            'numero_bastidor',
            'tipo_vehiculo',
            'cilindrada',
            'potencia',
            'combustible',
            'mma',
            'asientos',
            'ejes',
            'dni_propietario',
            'matricula',
            'fecha_matriculacion',
            'propietario',
            'trabajadores',
            'inspecciones'
        )


   
class LocalSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['precio', 'metros', 'anio_arrendamiento', 'duenio']

    def validate_precio(self, precio):
        if precio <= 0:
            raise serializers.ValidationError("El precio debe ser mayor a 0.")
        return precio

    def validate_metros(self, metros):
        if metros <= 0:
            raise serializers.ValidationError("Los metros deben ser mayores a 0.")
        return metros

    def validate_anio_arrendamiento(self, anio_arrendamiento):
        if anio_arrendamiento.year < 1900:
            raise serializers.ValidationError("El año de arrendamiento debe ser mayor a 1900.")
        return anio_arrendamiento

class LocalSerializerActualizarDuenio(serializers.ModelSerializer):
    class Meta:
        model = Local
        fields = ['duenio']

    def validate_duenio(self, duenio):
        if len(duenio.strip()) == 0:
            raise serializers.ValidationError("El nombre del dueño no puede estar vacío.")
        return duenio
        

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
            raise serializers.ValidationError('La fecha seleccionada no puede ser inferior a la actual')
        return fecha_propuesta
    
    def validate_estacion(self,estacion):
        if not estacion:
            raise serializers.ValidationError("Seleccione una estación válida.")
        return estacion
    
class CitaSerializerActualizarMatricula(serializers.ModelSerializer):
    class Meta:
        model = Cita
        fields = ["matricula"]
        
    def validate_matricula(self,matricula):
        citaMatricula = Cita.objects.filter(matricula=matricula).first()
        if(not citaMatricula is None and citaMatricula.id != self.instance.id):
            raise serializers.ValidationError('Ya existe una matricula con ese nombre')
        return matricula
 
 
class TrabajadorSerializerCreate(serializers.ModelSerializer):
    estacion=EstacionItvSerializer()
    class Meta:
        model = Trabajador
        fields = ['email', 'nombre', 'apellidos', 'puesto', 'sueldo', 'observaciones', 'estacion']


    def validate_nombre(self, nombre):
        if len(nombre) < 2:
            raise serializers.ValidationError("El nombre debe contener al menos 2 caracteres.")
        return nombre
    
    def validate_sueldo(self, sueldo):
        if sueldo is not None and sueldo < 0:
            raise serializers.ValidationError("El sueldo no puede ser negativo.")
        return sueldo

    def validate_puesto(self, puesto):
        if puesto not in ['EM', 'FR', 'DI']: 
            raise serializers.ValidationError("Seleccione un puesto válido.")
        return puesto

    def create(self, validated_data):
        estacion = self.initial_data.get("estacion")
        
        usuario = validated_data.get("usuario", None)

        if not usuario:
            raise serializers.ValidationError({'usuario': ['No puedo crear un trabajador sin crear un usario antes, me he pasado 2h intentando averiguar que pasa, ya no puedo cambiarlo']})

        try:
            trabajador = Trabajador.objects.create(
                email=validated_data["email"],
                nombre=validated_data["nombre"],
                apellidos=validated_data["apellidos"],
                puesto=validated_data["puesto"],
                sueldo=validated_data["sueldo"],
                observaciones=validated_data["observaciones"]
            )
        except Exception as e:
            print("No puedo crear un trabajador sin crear un usario antes, me he pasado 2h intentando averiguar que pasa, ya no puedo cambiarlo", str(e))
            raise serializers.ValidationError({"error": f"No se pudo crear el trabajador: {str(e)}"})

        for estaci in estacion:
                estacion_obj = EstacionItv.objects.get(id=estaci)
                trabajador.estacion.add(estacion_obj)
        return trabajador

    def update(self, instance, validated_data):
        estaciones = self.initial_data.get('estacion', [])

        if len(estaciones) < 1:
            raise serializers.ValidationError(
                {'estacion': ['Debe seleccionar al menos una estación']}
            )

        instance.email = validated_data.get("email", instance.email)
        instance.nombre = validated_data.get("nombre", instance.nombre)
        instance.apellidos = validated_data.get("apellidos", instance.apellidos)
        instance.puesto = validated_data.get("puesto", instance.puesto)
        instance.sueldo = validated_data.get("sueldo", instance.sueldo)
        instance.observaciones = validated_data.get("observaciones", instance.observaciones)

        instance.save()


        instance.estacion.clear() 
        for estacion_id in estaciones:
            estacion_obj = EstacionItv.objects.get(id=estacion_id)
            instance.estacion.add(estacion_obj)

        return instance

class TrabajadorSerializerActualizarPuesto(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ['puesto']

    def validate_puesto(self, puesto):
        if puesto not in ['EM', 'FR', 'DI']:
            raise serializers.ValidationError("Seleccione un puesto válido.")
        return puesto

class TrabajadorIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajador
        fields = ['id']
class VehiculoSerializerCreate(serializers.ModelSerializer): 
    trabajadores = TrabajadorIDSerializer(many=True)

    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'numero_bastidor', 'tipo_vehiculo', 'cilindrada',
                  'potencia', 'combustible', 'mma', 'asientos', 'ejes', 'dni_propietario',
                  'matricula', 'fecha_matriculacion', 'trabajadores']

    def validate_marca(self, marca):
        if len(marca) < 2:
            raise serializers.ValidationError("La marca debe contener al menos 2 caracteres.")
        return marca

    def validate_matricula(self, matricula):
        if len(matricula) > 7:
            raise serializers.ValidationError("La matrícula no puede tener más de 7 caracteres.")
        return matricula

    def validate_cilindrada(self, cilindrada):
        if cilindrada < 0:
            raise serializers.ValidationError("La cilindrada no puede ser negativa.")
        return cilindrada

    def create(self, validated_data):
        trabajadores_data = self.initial_data.get('trabajadores', [])
        if len(trabajadores_data) < 1:
            raise serializers.ValidationError({'trabajadores': ['Debe seleccionar al menos un trabajador.']})

        vehiculo = Vehiculo.objects.create(
            marca=validated_data["marca"],
            modelo=validated_data["modelo"],
            numero_bastidor=validated_data["numero_bastidor"],
            tipo_vehiculo=validated_data["tipo_vehiculo"],
            cilindrada=validated_data["cilindrada"],
            potencia=validated_data["potencia"],
            combustible=validated_data["combustible"],
            mma=validated_data["mma"],
            asientos=validated_data["asientos"],
            ejes=validated_data["ejes"],
            dni_propietario=validated_data["dni_propietario"],
            matricula=validated_data["matricula"],
            fecha_matriculacion=validated_data["fecha_matriculacion"],
        )

        trabajadores_ids = [trabajador["id"] for trabajador in trabajadores_data]
        trabajadores_objs = Trabajador.objects.filter(id__in=trabajadores_ids)

        vehiculo.trabajadores.set(trabajadores_objs)

        return vehiculo

    def update(self, instance, validated_data):
        trabajadores_data = self.initial_data.get('trabajadores', [])

        if len(trabajadores_data) < 1:
            raise serializers.ValidationError({'trabajadores': ['Debe seleccionar al menos un trabajador.']})

        instance.marca = validated_data.get("marca", instance.marca)
        instance.modelo = validated_data.get("modelo", instance.modelo)
        instance.numero_bastidor = validated_data.get("numero_bastidor", instance.numero_bastidor)
        instance.tipo_vehiculo = validated_data.get("tipo_vehiculo", instance.tipo_vehiculo)
        instance.cilindrada = validated_data.get("cilindrada", instance.cilindrada)
        instance.potencia = validated_data.get("potencia", instance.potencia)
        instance.combustible = validated_data.get("combustible", instance.combustible)
        instance.mma = validated_data.get("mma", instance.mma)
        instance.asientos = validated_data.get("asientos", instance.asientos)
        instance.ejes = validated_data.get("ejes", instance.ejes)
        instance.dni_propietario = validated_data.get("dni_propietario", instance.dni_propietario)
        instance.matricula = validated_data.get("matricula", instance.matricula)
        instance.fecha_matriculacion = validated_data.get("fecha_matriculacion", instance.fecha_matriculacion)

        instance.save()

        trabajadores_ids = [trabajador["id"] for trabajador in trabajadores_data]
        trabajadores_objs = Trabajador.objects.filter(id__in=trabajadores_ids)

        instance.trabajadores.set(trabajadores_objs)

        return instance
    
    
class VehiculoSerializerActualizarMatricula(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ['matricula']

    def validate_matricula(self, matricula):
        if len(matricula) > 7:
            raise serializers.ValidationError("La matrícula no puede tener más de 7 caracteres.")
        return matricula
    
class UsuarioSerializerRegistro(serializers.Serializer):
    
    username = serializers.CharField()
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    puesto=serializers.CharField(required=False,allow_blank=True)
    
    fecha_nacimiento = serializers.CharField(required=False, allow_blank=True)
    
    apellidos = serializers.CharField(required=False, allow_blank=True)
    dni = serializers.CharField(required=False, allow_blank=True)

    def validate_username(self, username):
        usuario = Usuario.objects.filter(username=username).first()
        if usuario:
            raise serializers.ValidationError('Ya existe ese usuario')
        return username

    def validate_email(self, email):
        regex_email = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(regex_email, email):
            raise serializers.ValidationError("El formato del email no es correcto")
        return email

    def validate_dni_unico(self,dni):
        cliente = Cliente.objects.filter(dni=dni).first()
        if cliente:
            raise serializers.ValidationError('Ya existe un cliente con este DNI')
        return dni
    
    def validate_dni(self, dni):
        regex_dni = r"^\d{8}[A-Z]$"
        if dni and not re.fullmatch(regex_dni, dni):
            raise serializers.ValidationError("El formato del DNI no es correcto")
        return dni

    def validate(self, data):
        if data.get("password1") != data.get("password2"):
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})
        return data
    
    def validate_fecha_nacimiento(self, fecha_nacimiento):
        if fecha_nacimiento:
            regex_fecha = r"^\d{4}-\d{2}-\d{2}$"
            if not re.fullmatch(regex_fecha, fecha_nacimiento):
                raise serializers.ValidationError("El formato de la fecha debe ser YYYY-MM-DD.")
        return fecha_nacimiento