from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Usuario (AbstractUser):
    ADMINISTRADOR = 1
    CLIENTE = 2
    TRABAJADOR = 3
    ROLES = (
        (ADMINISTRADOR,"administrador"),
        (CLIENTE,"cliente"),
        (TRABAJADOR,"trabajador")
    )
    rol = models.PositiveBigIntegerField(choices=ROLES,default=1)

class Cliente(models.Model):
    email=models.CharField(max_length=50,blank=True)
    nombre=models.CharField(max_length=50,blank=True)
    apellidos=models.CharField(max_length=50,blank=True)
    SEXO=[('M','Masculino'),('F','Femenino')]
    sexo=models.CharField(max_length=1,choices=SEXO)
    fecha_nacimiento=models.DateField(null=True)
    codigo_postal=models.IntegerField(null=True)
    domicilio=models.TextField(null=True)
    telefono=models.PositiveIntegerField(null=True)
    dni=models.CharField(max_length=9,unique=True, null=True)
    imagen = models.ImageField(upload_to='imagenes/',null=True, blank=True)
    
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.usuario.username + " " + self.apellidos

class Local(models.Model):
    precio=models.FloatField()
    metros=models.DecimalField(max_digits=50,decimal_places=3)
    anio_arrendamiento=models.DateField()
    duenio=models.CharField(max_length=50)
    
    def __str__(self):
        return self.duenio + " "+ str(self.metros)
    
class EstacionItv(models.Model):
    #relaciones
    local=models.OneToOneField(Local,on_delete=models.CASCADE,null=True)
    #
    nombre=models.CharField(max_length=50,unique=True)
    munipio=models.CharField(max_length=50)
    eficiencia_energetica=models.CharField(max_length=1)
    comunidad_autonoma=models.CharField(max_length=20)
    
    def __str__(self):
        return self.munipio + " "+ self.nombre
    
class Cita(models.Model):
    #relaciones
    cliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,related_name="cliente_cita")
    estacion=models.ForeignKey(EstacionItv,on_delete=models.CASCADE)
    #
    matricula=models.CharField(max_length=7)
    fecha_matriculacion=models.DateField(help_text="Este campo o el numero de bastidor debe estar relleno",null=True)
    numero_bastidor=models.CharField(max_length=17)
    TIPOINSPECCION=[
        ('PE','Periodica'),
        ('NOPE','NoPeriodica'),
        ('VETAX','VerificacionTaximetro'),
        ('VETAXV','VerificacionTaximetroCambioVehiculo')
        ]
    tipo_inspeccion=models.CharField(max_length=7,choices=TIPOINSPECCION)
    remolque=models.BooleanField(default=False)
    TIPOPAGO=[('TA','Tarjeta'),('EF','Efectivo')]
    tipo_pago=models.CharField(max_length=2,choices=TIPOPAGO)
    fecha_propuesta=models.DateField(null=True)
    hora_propuesta=models.TimeField(null=True)

    def __str__(self):
        return self.tipo_inspeccion 
    
class EmpresaExterna(models.Model):
    nombre=models.CharField(max_length=50,null=False)
    municipio=models.CharField(max_length=50)
    coste=models.FloatField(editable=True)
    cif=models.CharField(max_length=15,null=False)

    def __str__(self):
        return self.nombre + " "+ self.cif
        
class Maquinaria(models.Model):
    #relaciones
    iestacionItv=models.ForeignKey(EstacionItv,on_delete=models.CASCADE,related_name="estacionitv_Maquinaria")
    idmpresaExterna=models.ForeignKey(EmpresaExterna,on_delete=models.CASCADE,related_name="empresaexterna_Maquinaria")
    #
    nombre=models.CharField(max_length=50)
    TIPO=[('',''),('EM','Emisiones'),('FR','Frenos'),('DI','Direccion')]
    tipo=models.CharField(max_length=2,choices=TIPO)
    ultimo_mantenimiento=models.DateField(blank=True)
    funcionando=models.BooleanField(default=True)
    
class Trabajador(models.Model):
    #relaciones
    estacion=models.ManyToManyField(EstacionItv,related_name="estacionItv_trabajadores")
    usuario=models.OneToOneField(Usuario,on_delete=models.CASCADE)
    #
    email=models.CharField(max_length=50,blank=True)
    nombre=models.CharField(max_length=50,blank=True)
    apellidos=models.CharField(max_length=50,null=True)
    puesto=models.CharField(max_length=2,choices=Maquinaria.TIPO)
    sueldo=models.FloatField(editable=True,null=True)
    observaciones=models.TextField(null=True)
    
    def __str__(self):
        return self.usuario.username + " "
    
class Vehiculo(models.Model):
    #relaciones
    #Para relacionar vehiculo con trabajador usando la tabla intermedia Inspeccion
    trabajadores = models.ManyToManyField(Trabajador, through='Inspeccion' ,related_name="trabajador_Vehiculo")
    propietario = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='propietario_vehiculo')
    #
    fecha_matriculacion=models.DateField()
    marca=models.CharField(max_length=50)
    modelo=models.CharField(max_length=50)
    numero_bastidor=models.CharField(max_length=17)
    TIPOS_VEHICULOS_ITV = [
        ('tur', 'Turismo'),
        ('moto', 'Motocicleta'),
        ('cam', 'Camión'),
        ('bus', 'Autobús'),
        ('furg', 'Furgoneta'),
        ('quad', 'Quad'),
        ('tracto', 'Tractor')
    ]
    tipo_vehiculo=models.CharField(max_length=6,choices=TIPOS_VEHICULOS_ITV)
    cilindrada=models.IntegerField()
    potencia=models.IntegerField()
    TIPOS_COMBUSTIBLE = [
        ('gas', 'Gasolina'),
        ('die', 'Diésel'),
        ('ele', 'Eléctrico'),
        ('hib', 'Híbrido'),
        ('gpl', 'GLP (Gas Licuado)'),
        ('gnv', 'GNC (Gas Natural)')
    ]
    combustible=models.CharField(max_length=3,choices=TIPOS_COMBUSTIBLE)
    mma=models.PositiveIntegerField()
    asientos=models.PositiveSmallIntegerField()
    ejes=models.PositiveSmallIntegerField()
    dni_propietario=models.CharField(max_length=9)
    matricula=models.CharField(max_length=7)
    
    def __str__(self):
        return self.marca + " "+ self.modelo
    
class Inspeccion(models.Model):
    #relaciones
    #
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE,related_name="trabajador_Inspeccion")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,related_name="vehiculo_Inspeccion")
    #
    fecha_inspeccion = models.DateField(default=timezone.now)
    resultado_inspeccion = models.CharField(max_length=100)
    notas_inspeccion = models.TextField()
    cliente_puntual=models.BooleanField(default=True)
    
         
class Factura(models.Model):
    #relaciones
    #
    inspeccion=models.OneToOneField(Inspeccion,on_delete=models.CASCADE,related_name="inspeccion_Factura")
    #
    importe=models.DecimalField(max_digits=50,decimal_places=2)
    pagado=models.BooleanField(default=False)
    fecha_emision_factura= models.DateField(default=timezone.now)
    observaciones=models.TextField()