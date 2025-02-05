from django import forms
from django.forms import ModelForm
from .models import *
from datetime import *
import re 
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
    
class CitaForm(ModelForm):
    class Meta:
        model = Cita
        fields = ('estacion','matricula','fecha_matriculacion','numero_bastidor','tipo_inspeccion','remolque','tipo_pago','fecha_propuesta','hora_propuesta')
        labels = {
            "fecha_matriculacion": "Fecha de Matriculación",
            "numero_bastidor": "Número de Bastidor",
            "tipo_inspeccion": "Tipo de Inspección",
            "tipo_pago": "Tipo de Pago",
            "fecha_propuesta": "Fecha Propuesta",
            "hora_propuesta": "Hora Propuesta",
        }
        widgets = {
            "fecha_matriculacion": forms.SelectDateWidget(),
            "fecha_propuesta": forms.SelectDateWidget(),
            "hora_propuesta": forms.TimeInput(attrs={'type': 'time'}),
            # "cliente":forms.HiddenInput()
        }
        help_texts = {
            "matricula": "Introduce la matrícula en formato válido (máximo 7 caracteres).",
            "fecha_matriculacion": "Este campo o el número de bastidor debe estar relleno.",
        }

    def clean(self):
        cleaned_data = super().clean()
        matricula = cleaned_data.get("matricula")
        numero_bastidor = cleaned_data.get("numero_bastidor")
        
        # Validación para asegurarse de que al menos uno de los dos campos esté lleno
        if not matricula and not numero_bastidor:
            self.add_error("matricula","Debes rellenar al menos la matrícula o el número de bastidor.")
            self.add_error("numero_bastidor","Debes rellenar al menos la matrícula o el número de bastidor.")
        
        return cleaned_data
    
class BusquedaAvanzadaCita(forms.Form):
    matricula = forms.CharField(
        required=False,
        label="Matrícula del vehículo",
        max_length=7,
    )
    tipo_inspeccion = forms.ChoiceField(
        required=False,
        label="Tipo de Inspección",
        choices=[('', 'Seleccione un tipo de inspección')] + Cita.TIPOINSPECCION,
    )
    fecha_propuesta = forms.DateField(
        required=False,
        label="Fecha propuesta",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    
    def clean(self):
        super().clean()
        
        matricula = self.cleaned_data.get("matricula")
        tipo_inspeccion = self.cleaned_data.get("tipo_inspeccion")
        fecha_propuesta = self.cleaned_data.get("fecha_propuesta")
        
        # Validación para que al menos un campo esté lleno
        if not matricula and not tipo_inspeccion and not fecha_propuesta:
            self.add_error("matricula","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("tipo_inspeccion","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("fecha_propuesta","Debe introducir al menos un valor en un campo del formulario")
        
        # Validación de longitud de matrícula
        if matricula and len(matricula) > 7:
            self.add_error("matricula", "La matrícula no puede tener más de 7 caracteres.")
        
        # Validación de fecha futura
        if fecha_propuesta and fecha_propuesta < timezone.now().date():
            self.add_error("fecha_propuesta", "La fecha propuesta no puede ser una fecha pasada.")
        
        return self.cleaned_data

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        labels = {
            "fecha_nacimiento" : ("Fecha de nacimiento"),
            "codigo_postal": ("Codigo postal")
        }
        help_texts = {
            "nombre" : ("50 caracteres como máximo"),
            "apellidos" : ("50 caracteres como máximo"),
            "correo" : ("50 caracteres como máximo"),
            "dni" : ("9 caracteres como máximo")
        }
        widgets = {
            "fecha_nacimiento" : forms.SelectDateWidget(),
            "domicilio" : forms.TextInput(),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        localized_fields = ["fecha_nacimiento"]
        
    def clean(self):
        
        super().clean()
        dni=self.cleaned_data.get('dni')
        
        #VALIDAMOS DNI
        
        expresion = "^[0-9]{8}[A-Z]$"
        
        if(not re.search(expresion,dni)):
            self.add_error("dni","El formato del dni no es correcto")
        
        dniCliente=Cliente.objects.filter(dni=dni).first()
        
        if(not dniCliente is None):
            if(not self.instance is None and dniCliente.id == self.instance.id):
                pass
            else:
                self.add_error("dni","El dni ya existe en la base de datos") 
           
        return self.cleaned_data

class BusquedaAvanzadaCliente(forms.Form):
    nombre=forms.CharField(required=False,label="Nombre del usuario")
    dni=forms.CharField(required=False,label="Dni del usuario")
    fecha_nacimiento=forms.DateField(required=False,label="Fecha de nacimiento"
                                     ,widget=forms.DateInput(format="%Y-%m-%d", 
                                                            attrs={"type": "date"},
                                                            )
                                    )
    
    def clean(self):
        super().clean()
        
        nombre=self.cleaned_data.get("nombre")
        dni=self.cleaned_data.get("dni") 
        fecha_nacimiento=self.cleaned_data.get("fecha_nacimiento") 
        
        if(nombre == "" and dni == "" and fecha_nacimiento is None):
            self.add_error("nombre","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("dni","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("fecha_nacimiento","Debe introducir al menos un valor en un campo del formulario")
        else:
            if(nombre and len(nombre)>50):
                self.add_error("nombre","No puede introducir mas de 50 caracteres")
            
            if(fecha_nacimiento is not None and fecha_nacimiento>=timezone.now().date()):
                self.add_error("fecha_nacimiento","La fecha de nacimiento no puede ser mayor a la de hoy")
            
            expresion = "^[0-9]{8}[A-Z]$"       
            if(dni and not re.search(expresion,dni)):
                self.add_error("dni","El formato del dni no es correcto")
                
        return self.cleaned_data
    
    #INSPECCION

class InspeccionForm(ModelForm):
    class Meta:
        model=Inspeccion
        fields='fecha_inspeccion','resultado_inspeccion','notas_inspeccion','cliente_puntual'
        labels= {
            "fecha_inspeccion" : ("Fecha de la inspección"),
            "resultado_inspeccion" : ("Resultado de la inspección"),
            "notas_inspeccion" : ("Notas de la inspección"),
            "cliente_puntual" : ("¿Es un cliente habitual?"),
            # "trabajador" : ("Trabajador a cargo"),
                # Van a salir solo los vehiculos que estan en su estacion
            # "vehiculo" : ("Vehiculo inspeccionado"),
        }
        widgets = {
            "fecha_inspeccion" : forms.SelectDateWidget(),
            "notas_inspeccion" : forms.TextInput(),
            "cliente_puntual":forms.CheckboxInput(),
            # "trabajador" : forms.Select(),
        }
    
    def clean(self):
        
        super().clean()
        
        fecha_inspeccion =self.cleaned_data.get('fecha_inspeccion') 
        notas_inspeccion = self.cleaned_data.get('notas_inspeccion') 
        
        if(fecha_inspeccion>timezone.now().date()):
            self.add_error("fecha_inspeccion","La fecha de la inspeccion no puede ser superior a la actual")
            
        if(notas_inspeccion==" "):
            self.add_error("notas_inspeccion","Las notas de la inspeccion no pueden estar vacias")
            
        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(InspeccionForm, self).__init__(*args, **kwargs)
        
        trabajador = Trabajador.objects.get(id=self.request.user.trabajador.id)
        estaciones = trabajador.estacion.all()
        vehiculos_disponibles = Vehiculo.objects.filter(trabajadores__estacion__in=estaciones).distinct()
        self.fields["vehiculo"] = forms.ModelChoiceField(
            queryset=vehiculos_disponibles,
            widget=forms.Select,
            required=True,
            empty_label="Seleccione un vehículo"
        )
         
class BusquedaAvanzadaInspeccion(forms.Form):
    
    resultado_inspeccion=forms.CharField(required=False,label="Resultado de la inspeccion")
    notas_inspeccion=forms.CharField(required=False,label="Notas de la inspeccion")
    fecha_inspeccion=forms.DateField(required=False,label="Fecha de la inspeccion",
                                     widget=forms.DateInput(format="%Y-%m-%d", 
                                                            attrs={"type": "date"},))
    
    def clean(self):
        
        super().clean()
        
        resultado_inspeccion=self.cleaned_data.get("resultado_inspeccion")
        notas_inspeccion=self.cleaned_data.get("notas_inspeccion") 
        fecha_inspeccion=self.cleaned_data.get("fecha_inspeccion") 
        
        if(resultado_inspeccion =="" and notas_inspeccion=="" and fecha_inspeccion is None):
            self.add_error("resultado_inspeccion","Debes rellenar algun dato")
            self.add_error("notas_inspeccion","Debes rellenar algun dato")
            self.add_error("fecha_inspeccion","Debes rellenar algun dato")
        else:
            if resultado_inspeccion and ('_' in resultado_inspeccion):
                self.add_error("resultado_inspeccion","Este campo no puede contener una _")
            if notas_inspeccion and ('!' in notas_inspeccion):
                self.add_error("notas_inspeccion","Este campo no permite un caracter '!'")
            if fecha_inspeccion is not None and fecha_inspeccion>timezone.now().date():
                self.add_error("fecha_inspeccion","La fecha de la inspeccion no puede ser superior a la de hoy")
        
        return self.cleaned_data 
          
    #VEHICULO

class VehiculoForm(ModelForm):
    class Meta:
        model=Vehiculo
        fields=('trabajadores','fecha_matriculacion','marca','modelo','numero_bastidor','tipo_vehiculo','cilindrada','potencia','combustible','mma','asientos','ejes','dni_propietario','matricula')
        labels = {
            "fecha_matriculacion": ("Fecha de matriculación"),
            "marca": ("Marca del vehículo"),
            "modelo": ("Modelo del vehículo"),
            "numero_bastidor": ("Número de bastidor"),
            "tipo_vehiculo": ("Tipo de vehículo (ITV)"),
            "cilindrada": ("Cilindrada (cc)"),
            "potencia": ("Potencia (CV)"),
            "combustible": ("Tipo de combustible"),
            "mma": ("Masa Máxima Autorizada (kg)"),
            "asientos": ("Número de asientos"),
            "ejes": ("Número de ejes"),
            "dni_propietario": ("DNI del propietario"),
            "matricula": ("Matrícula"),
            "trabajadores" : ("Trabajadores")
        }
        help_texts = {
            "trabajadores" : ("Manten pulsada la tecla control para seleccionar varios elementos"),
        }
        widgets = {
            "fecha_matriculacion" : forms.SelectDateWidget(),
            "trabajadores" : forms.SelectMultiple(),
            "tipo_vehiculo" : forms.Select(),
            "combustible" : forms.Select(),
            "numero_bastidor":forms.NumberInput
        }
        localized_fields = ["fecha_matriculacion"]
        
    def clean(self):
        super().clean()
        
        tipo_vehiculo=self.cleaned_data.get("tipo_vehiculo")
        ejes=self.cleaned_data.get("ejes")
        asientos=self.cleaned_data.get("asientos")
        
        matricula=self.cleaned_data.get("matricula")
        
        if(tipo_vehiculo=="moto" and asientos>1):
            self.add_error("asientos","Para el tipo de vehiculo Motocicleta solo puedes escoger un asiento")
            
        if(tipo_vehiculo=="bus" and ejes<=2):
            self.add_error("ejes","Revisa el tipo de vehiculo, el que has seleccionado tiene mas de 2 ejes")
            
        matriculaVehiculo=Vehiculo.objects.filter(matricula=matricula).first()
        if (not matriculaVehiculo is None):
            if(not self.instance is None and matriculaVehiculo.id == self.instance.id):
                pass
            else:
                self.add_error("matricula","Esta matricula ya esta registrada") 
            
        return self.cleaned_data

class BusquedaAvanzadaVehiculo(forms.Form):
    
    marca=forms.CharField(required=False,label="Marca")
    potencia=forms.IntegerField(required=False,label="Potencia")
    matricula=forms.CharField(required=False,label="Matricula")
    
    def clean(self):
        
        super().clean()
        
        marca=self.cleaned_data.get("marca")
        potencia=self.cleaned_data.get("potencia") 
        matricula=self.cleaned_data.get("matricula") 
        
        if(marca == "" and potencia is None and matricula == ""):
            self.add_error("marca","Debes rellenar algun dato")
            self.add_error("potencia","Debes rellenar algun dato")
            self.add_error("matricula","Debes rellenar algun dato")
        else:
            if marca and ('_' in marca):
                self.add_error("marca","Este campo no puede contener una _")
            if potencia is not None and (potencia<0):
                self.add_error("potencia","La potencia tiene que ser mayor que 0")
            if matricula and ('!' in matricula):
                self.add_error("matricula","Este campo no permite un caracter '!'")
        
        return self.cleaned_data 
    
    #LOCAL   

class LocalForm(ModelForm):
    class Meta:
        model=Local
        fields='__all__'
        labels = {
            "precio": ("Precio del local"),
            "metros": ("Metros del local"),
            "anio_arrendamiento": ("Año en el que se arrendó"),
            "duenio": ("Dueño del local")
        }
        widgets = {
            "anio_arrendamiento" : forms.SelectDateWidget(),
            "metros" : forms.NumberInput,
        }
        localized_fields = ["anio_arrendamiento"]
        
    def clean(self):
        super().clean()
        precio=self.cleaned_data.get("precio")
        metros=self.cleaned_data.get("metros")
        
        if (precio<0):
            self.add_error("precio","El precio no puede ser negativo")
        if(metros<0):
            self.add_error("metros","Los metros no pueden ser negativos")
            
        return self.cleaned_data
    
class BusquedaAvanzadaLocal(forms.Form):
    
    precio=forms.FloatField(required=False,label="Precio")
    metros=forms.DecimalField(required=False,label="Metros")
    anio_arrendamiento=forms.DateField(required=False,label="Año del arrendamiento",
                                    widget=forms.DateInput(format="%Y-%m-%d", 
                                                        attrs={"type": "date"},))
    
    def clean(self):
        
        super().clean()
        
        precio=self.cleaned_data.get("precio")
        metros=self.cleaned_data.get("metros") 
        anio_arrendamiento=self.cleaned_data.get("anio_arrendamiento") 
        
        if(precio is None and metros is None and anio_arrendamiento is None):
            self.add_error("precio","Debes rellenar algun dato")
            self.add_error("metros","Debes rellenar algun dato")
            self.add_error("anio_arrendamiento","Debes rellenar algun dato")
        else:
            if precio is not None and (precio<0):
                self.add_error("precio","Este campo no puede ser negativo")
            if metros is not None and (metros<0):
                self.add_error("metros","La potencia no puede ser negativa")
            if anio_arrendamiento is not None and anio_arrendamiento>timezone.now().date():
                self.add_error("anio_arrendamiento","La fecha no puede ser superior a la actual")
        
        return self.cleaned_data 

    #ESTACION    

class EstacionForm(ModelForm):
    class Meta:
        model=EstacionItv
        fields='__all__'
        labels = {
            "nombre": ("Nombre de la estacion"),
            "munipio": ("Municipio de la estacion"),
            "eficiencia_energetica": ("Eficiencia energetica"),
            "comunidad_autonoma": ("Comunidad autonoma"),
            "local": ("Locales"),
        }
        help_texts = {
            "eficiencia_energetica" : ("Una sola letra"),
        }
        widgets = {
            "local" : forms.Select()
        }        
        
    def clean(self):
        comunidad_autonoma=self.cleaned_data.get("comunidad_autonoma")
        eficiencia_energetica=self.cleaned_data.get("eficiencia_energetica")
        
        if(comunidad_autonoma[0].islower()):
            self.add_error("comunidad_autonoma","La primera letra tiene que ser mayuscula")
        
        if(eficiencia_energetica==" "):
            self.add_error("eficiencia_energetica","El unico caracter no puede ser un espacio")
        return self.cleaned_data
    
class BusquedaAvanzadaEstacion(forms.Form):
   
    nombre=forms.CharField(required=False,label="Nombre")
    munipio=forms.CharField(required=False,label="Municipio")
    comunidad_autonoma=forms.CharField(required=False,label="Comunidad autonoma")
    
    def clean(self):
        
        super().clean()
        
        nombre=self.cleaned_data.get("nombre")
        munipio=self.cleaned_data.get("munipio") 
        comunidad_autonoma=self.cleaned_data.get("comunidad_autonoma") 
        
        if(nombre =="" and  munipio =="" and comunidad_autonoma ==""):
            self.add_error("nombre","Debes rellenar algun dato")
            self.add_error("munipio","Debes rellenar algun dato")
            self.add_error("comunidad_autonoma","Debes rellenar algun dato")
        else:
            if nombre and (not nombre[0].isupper()):
                self.add_error("nombre","El nombre debe empezar por una mayuscula")
            if munipio and (munipio[0].isdigit()):
                self.add_error("munipio","El primer caracter no puede ser un numero")
            if comunidad_autonoma and ('_' in comunidad_autonoma):
                self.add_error("comunidad_autonoma","La comunidad autonoma no puede contener un '_'")
        
        return self.cleaned_data 

    #TRABAJADOR            

class TrabajadorForm(ModelForm):
    class Meta:
        model=Trabajador
        fields='__all__'
        labels = {
            "nombre": ("Nombre del trabajador"),
            "apellidos": ("Apellidos del trabajador"),
            "puesto": ("Puesto del trabajador"),
            "sueldo": ("Sueldo del trabajador"),
            "observaciones": ("Observaciones del trabajador"),
            "estacion": ("Estacion del trabajador"),  
        }
        widgets = {
            "estacion" : forms.SelectMultiple()
        }
    
    def clean(self):
        sueldo=self.cleaned_data.get("sueldo")
        observaciones=self.cleaned_data.get("observaciones")
        caracter="!"
        
        if caracter in observaciones:
            self.add_error("observaciones","El campo observaciones no puede contener un '!'")
            
        if sueldo < 0:
            self.add_error("sueldo","El sueldo no puede ser negativo")
            
        return self.cleaned_data
    
class BusquedaAvanzadaTrabajador(forms.Form):
    
    nombre=forms.CharField(required=False,label="Nombre")
    sueldo=forms.FloatField(required=False,label="Sueldo")
    puesto=forms.CharField(required=False,label="Puesto")
    
    def clean(self):
        
        super().clean()
        
        nombre=self.cleaned_data.get("nombre")
        sueldo=self.cleaned_data.get("sueldo") 
        puesto=self.cleaned_data.get("puesto") 
        
        if(nombre =="" and  sueldo is None and puesto ==""):
            self.add_error("nombre","Debes rellenar algun dato")
            self.add_error("sueldo","Debes rellenar algun dato")
            self.add_error("puesto","Debes rellenar algun dato")
        else:
            if nombre and (len(nombre) < 3 or any(char.isdigit() for char in nombre)):
                self.add_error("nombre","El nombre debe tener al menos 3 caracteres y no puede contener números")
            if not sueldo is None and (sueldo <= 10):
                self.add_error("sueldo","El sueldo debe ser mayor a 10")
            if puesto and (char in "@#$%&*" for char in puesto):
                self.add_error("puesto","El puesto no puede contener caracteres especiales como @, #, $, %, etc")
        
        return self.cleaned_data 

#REGISTRO

class RegistroForm(UserCreationForm):
    roles = (
        (0,"Seleccione un tipo de rol"),
        (Usuario.CLIENTE,"cliente"),
        (Usuario.TRABAJADOR,"trabajador")        
    )
    
    rol= forms.ChoiceField(choices=roles)
    
    fecha_nacimiento=forms.DateField(required=False)
    apellidos=forms.CharField(required=False)
    dni=forms.CharField(required=False)
       
    tipo=(('',''),('EM','Emisiones'),('FR','Frenos'),('DI','Direccion'))
    puesto=forms.ChoiceField(choices=tipo,required=False)
    
    class Meta:
        model = Usuario
        fields = ('username','email','password1','password2','rol')
        
    def clean(self):
        
        super().clean()
        
        fecha_nacimiento=self.cleaned_data.get("fecha_nacimiento")
        apellidos=self.cleaned_data.get("apellidos")
        dni=self.cleaned_data.get('dni')
        
        expresion = "^[0-9]{8}[A-Z]$"        
        if(dni !="" and not re.search(expresion,dni)):
            self.add_error("dni","El formato del dni no es correcto")
            
        if(fecha_nacimiento is not None and fecha_nacimiento>timezone.now().date()):
            self.add_error("fecha_nacimiento","La fecha de nacimiento no puede ser superior a la actual")
            
        if (apellidos!="" and '_' in apellidos):
            self.add_error("apellidos","Este campo no puede contener un _")        
        
        puesto=self.cleaned_data.get("puesto")
        
        return self.cleaned_data
        
