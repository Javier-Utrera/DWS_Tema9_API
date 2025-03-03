# DWS_Tema3_AplicacionWeb

## Explicación de mi aplicación web

Esta aplicación está enfocada en la gestión del servicio ITV a nivel autonómico. Un cliente, que no necesariamente tiene que ser el dueño del vehículo a inspeccionar, puede pedir una cita en la ITV que desee. Su vehículo será inspeccionado por trabajadores que generarán un resultado de la inspección y su correspondiente factura para el pago.

---

## Modelos, atributos y parámetros

### **Cliente**
Modelo que representa a los clientes de la ITV.

- **Atributos:**
  - `nombre`: CharField (máx. 50 caracteres). Almacena el nombre del cliente.
  - `apellidos`: CharField (opcional, máx. 50 caracteres).
  - `sexo`: CharField con `choices` ('M' o 'F').
  - `fecha_nacimiento`: DateField.
  - `codigo_postal`: IntegerField.
  - `domicilio`: TextField.
  - `correo`: EmailField con validación automática.
  - `telefono`: PositiveIntegerField.
  - `dni`: CharField único (9 caracteres).
  - `dueño`: CharField (50 caracteres), almacena el dueño del local.

---

### **Local**
Modelo que representa los locales donde se pueden establecer estaciones ITV.

- **Atributos:**
  - `precio`: FloatField. Precio del alquiler.
  - `metros`: DecimalField (máx. 50 dígitos, 3 decimales).
  - `anio_arrendamiento`: DateField.

---

### **EstacionItv**
Modelo de las estaciones ITV.

- **Relaciones:**
  - `id_local`: Relación OneToOne con el modelo `Local`.

- **Atributos:**
  - `nombre`: CharField único (50 caracteres).
  - `municipio`: CharField (50 caracteres).
  - `eficiencia_energetica`: CharField (1 carácter, como A, B, C...).
  - `comunidad_autonoma`: CharField.

---

### **Cita**
Modelo que representa las citas para la inspección de vehículos.

- **Relaciones:**
  - `id_cliente`: ForeignKey a `Cliente`.
  - `id_estacion`: ForeignKey a `EstacionItv`.

- **Atributos:**
  - `matricula`: CharField (7 caracteres).
  - `fecha_matriculacion`: DateField.
  - `numero_bastidor`: CharField (17 caracteres).
  - `tipo_inspeccion`: CharField con `choices` (ej.: 'PE', 'NOPE', 'VETAX').
  - `remolque`: BooleanField (por defecto `False`).
  - `tipo_pago`: CharField (`choices`: tarjeta o efectivo).
  - `fecha_propuesta`: DateField.
  - `hora_propuesta`: TimeField.

---

### **EmpresaExterna**
Modelo que representa las empresas externas que mantienen las máquinas de la ITV.

- **Atributos:**
  - `nombre`: CharField.
  - `municipio`: CharField.
  - `coste`: FloatField (editable).
  - `cif`: CharField.

---

### **Maquinaria**
Modelo que representa la maquinaria usada en estaciones ITV.

- **Relaciones:**
  - `id_estacionItv`: ForeignKey a `EstacionItv`.
  - `id_empresaExterna`: OneToOneField a `EmpresaExterna`.

- **Atributos:**
  - `nombre`: CharField.
  - `tipo`: CharField (`choices`: emisiones, frenos, dirección).
  - `ultimo_mantenimiento`: DateField (opcional).
  - `funcionando`: BooleanField (por defecto `True`).

---

### **Trabajador**
Modelo que representa a los trabajadores de las estaciones ITV.

- **Relaciones:**
  - `id_estacion`: ManyToManyField con `EstacionItv`.
  - `jefe`: ManyToManyField recursivo (`self`).

- **Atributos:**
  - `nombre`: CharField.
  - `apellidos`: CharField.
  - `puesto`: CharField con `choices`.
  - `sueldo`: FloatField.
  - `observaciones`: TextField.

---

### **Vehiculo**
Modelo que representa los vehículos inspeccionados.

- **Relaciones:**
  - `trabajadores`: ManyToManyField con `Trabajador` (a través de `Inspeccion`).

- **Atributos:**
  - `fecha_matriculacion`: DateField.
  - `marca`, `modelo`, `numero_bastidor`: CharField.
  - `tipo_vehiculo`: CharField (`choices`).
  - `cilindrada`, `potencia`: IntegerField.
  - `combustible`: CharField (`choices`: gasolina, diésel, eléctrico...).
  - `mma`: PositiveIntegerField.
  - `asientos`, `ejes`: PositiveSmallIntegerField.
  - `dni_propietario`, `matricula`: CharField.

---

### **Inspeccion**
Modelo que representa las inspecciones realizadas.

- **Relaciones:**
  - `trabajador`: ForeignKey a `Trabajador`.
  - `vehiculo`: ForeignKey a `Vehiculo`.

- **Atributos:**
  - `fecha_inspeccion`: DateField (por defecto `timezone.now`).
  - `resultado_inspeccion`, `notas_inspeccion`: CharField y TextField.
  - `cliente_puntual`: BooleanField (por defecto `True`).

---

### **Factura**
Modelo que representa las facturas generadas.

- **Relaciones:**
  - `id_inspeccion`: OneToOneField con `Inspeccion`.

- **Atributos:**
  - `importe`: DecimalField.
  - `pagado`: BooleanField.
  - `fecha_emision_factura`: DateField.
  - `observaciones`: TextField.

---

## Vistas

1. **Lista de Clientes**: Ordenados por sexo, nombre y fecha de nacimiento.
2. **Citas de un Cliente**: Muestra citas asociadas a un cliente.
3. **Estaciones con Locales**: Lista estaciones y sus locales.
4. **Trabajadores de Estación**: Muestra trabajadores de una estación.
5. **Inspecciones de Vehículo**: Lista inspecciones de un vehículo por matrícula.
6. **Maquinaria y Empresa**: Detalle de maquinaria y su empresa asociada.
7. **Citas por Rango de Fechas**: Cita más reciente en un rango de años.
8. **Conteo de Vehículos**: Cuenta vehículos por combustible.
9. **Citas de una Estación**: Filtra citas por cliente y tipo.
10. **Vehículos sin Trabajadores**: Lista vehículos sin trabajadores.

---

## Widgets en Formularios

- `forms.SelectDateWidget`
- `forms.TextInput`
- `forms.DateInput`
- `forms.CheckboxInput`
- `forms.Select`
- `forms.SelectMultiple`
- `forms.NumberInput`

---

## Validaciones en Formularios

Se incluyen validaciones específicas para campos como DNI, fechas, resultados y relaciones.

---

## Instalación de Pillow para manejo de imágenes

1. Crear carpeta `media/imagenes` en la raíz del proyecto.
2. Agregar `Pillow~=11.0.0` al archivo `requirements.txt`.
3. Configurar modelos y formularios para admitir campos de imágenes.


# Funcionalidades Nuevas Implementadas

## TEMA 7: PERMISOS

### Datos:
He tenido que crear un CRUD nuevo para el usuario "cliente". En la entrega anterior no había tenido en cuenta que casi todo lo que se podía crear con mis CRUDs era para el administrador. Ahora he detallado dos tipos de usuarios adicionales: "Cliente" y "Trabajador". 

- El usuario **cliente** puede usar los CRUDs de **Citas** y **Vehículo**.
- El usuario **trabajador** puede usar el CRUD de **Inspección**.

---

## 1. Tipos de Usuarios Claramente Diferenciados  
He creado un nuevo modelo `Usuario` donde he detallado, además del usuario administrador, dos usuarios más: **Cliente** y **Trabajador**.

```python
ROLES = (
    (ADMINISTRADOR, "administrador"),
    (CLIENTE, "cliente"),
    (TRABAJADOR, "trabajador"),
)
```

---

## 2. Control de Permisos y Autenticación en Vistas  
En cada vista, se ha implementado el control de permisos para verificar si el usuario está logueado o no, y si tiene permisos para acceder a esa vista.

Aunque hay CRUDs donde mis usuarios no pueden acceder, les he asignado permisos de todas formas.

Cuando usamos el @permission ya se comprueba que el usuario este autenticado antes de comprobar el permiso, si queremos dejarlo mas detallado podriamos añadirle el 
```python
@login_required
```
Si no con este nos valdria
```python
@permission_required('ITV.add_cita')
```

---

## 3. Control de Permisos en Plantillas  
En cada template (vista y formulario), se ha controlado si el usuario está logueado y si tiene permisos para acceder o interactuar con los formularios y las vistas.  

En el template `menu.html`, he controlado qué bloques de URLs están accesibles para los distintos tipos de usuarios.

```html
{% if request.user.is_authenticated and perms.ITV.add_cita %}
```

---

## 4. Variables Guardadas en la Sesión  
Se han incluido al menos cuatro variables que se guardan en la sesión y que aparecen siempre en la cabecera de la página. Estas variables se eliminan cuando el usuario se desloguea.

En la función `index`, he creado 4 variables para mostrarlas en el template `menu.html`. En esta función, compruebo si existen dichas variables cuando el usuario entra en la página web. Si el usuario no pertenece a la aplicación (con `request.user.is_anonymous`), solo se crea la fecha de inicio de sesión. Si pertenece, se crean las demás variables.

Para borrar las variables de la sesión al hacer logout, he observado en el depurador que se eliminan automáticamente cuando el usuario se desloguea.

---

## 5. Registro de Usuarios y Validaciones  
He implementado un sistema de registro para los distintos tipos de usuario (excepto el administrador). Este sistema incluye validaciones específicas para controlar que, dependiendo del tipo de usuario, se asignen valores correspondientes.

Al registrar un usuario, según el tipo de usuario que se va a registrar, primero se le asigna al grupo correspondiente y luego se crea el usuario si no hay errores en las validaciones.

Para mostrar y ocultar campos, he usado un script `campos.js`. Me ha costado un par de intentos asegurarme de que, en caso de que el usuario tenga errores de validación y la página se recargue, los campos mostrados y ocultados permanezcan igual.

---

## 6. Login y Logout de Usuario  
Se ha implementado un sistema de login y logout para los usuarios.

He usado el sistema de login y logout proporcionado por Django, incluyendo en `urls.py` dentro de `mysite`:

```python
path('accounts/', include('django.contrib.auth.urls'))
```

Se ha tenido en cuenta la configuración en `settings.py`, además de crear el template `login.html` y controlar que, si un usuario está logueado, no le aparezca el botón de login, sino el botón de logout.

---

## 7. Variación de Contenido en Formularios Según el Usuario Logueado  
En un formulario, se ha creado una funcionalidad que hace que el contenido de algún campo `ManyToMany` o `ManyToOne` varíe dependiendo del usuario logueado.

Esta funcionalidad la he implementado cuando un trabajador crea una inspección. En mi aplicación, un trabajador puede trabajar en varias estaciones de ITV a la vez, por lo que he decidido que solo pueda realizar inspecciones en los vehículos que están en las estaciones donde trabaja.

Para ello, he utilizado un formulario de inspección `ModelForm`, pero usando el `request` para crear un campo que no importa automáticamente del modelo.

```python
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
```

---

## 8. Registro de Usuario en Formularios de Creación  
En los formularios de creación, se incluye siempre el usuario que crea el registro a través de la sesión del usuario.

Para no cambiar el tipo de formulario que ya tenía implementado, he optado por no incluir el campo del cliente o trabajador en el formulario de creación. 

Cuando Django comprueba que los datos del formulario son válidos, creo la cita "manualmente" y asigno el cliente al objeto `Cita`.

```python
cita = Cita.objects.create(
    estacion=formulario.cleaned_data.get('estacion'),
    matricula=formulario.cleaned_data.get('matricula'),
    numero_bastidor=formulario.cleaned_data.get('numero_bastidor'),
    tipo_inspeccion=formulario.cleaned_data.get('tipo_inspeccion'),
    remolque=formulario.cleaned_data.get('remolque'),
    tipo_pago=formulario.cleaned_data.get('tipo_pago'),
    fecha_matriculacion=formulario.cleaned_data.get('fecha_matriculacion'),
    fecha_propuesta=formulario.cleaned_data.get('fecha_propuesta'),
    hora_propuesta=formulario.cleaned_data.get('hora_propuesta'),
    cliente=request.user.cliente,
)
cita.save()
```

---

## 9. Filtrado de Contenido en Formularios de Búsqueda Según Usuario Logueado  
Se ha implementado una funcionalidad en un formulario de búsqueda en el que el contenido se filtra de acuerdo con el usuario que está logueado. Esto permite que solo se muestren los registros relacionados con el usuario actual, mejorando la personalización de la búsqueda.

En las vistas de crear y listar contenido, antes mostraba todos los registros. Ahora he modificado esas vistas para que solo muestre los registros asociados al usuario logueado.

```python
citas = Cita.objects.select_related("cliente", "estacion")
if(request.user.rol == 2) :
    cliente = Cliente.objects.get(id=request.user.cliente.id)
    citas = citas.filter(cliente_id=cliente.id).all()
else :
    citas = citas.all()
```


## 10. Implementación de Funcionalidad de Reinicio de Contraseña  
Se ha implementado una funcionalidad de reinicio de contraseña utilizando las herramientas proporcionadas por Django. Aunque en la aplicación local no se permite el envío de correos electrónicos, Django ofrece una manera de generar un enlace de recuperación de contraseña sin necesidad de enviar un email real. Se ha utilizado el sistema de autenticación de Django para permitir a los usuarios restablecer su contraseña de forma segura mediante un enlace generado.

Para realizar esta funcion vamos a indicar en el settings.py que a la hora de enviar correos de recuperacion, estos no sean correos reales, si no que nos redirija esos "correos" a la consola, ademas del cuerpo del correo, veremos lo que nos interesa, el enlace para modificar la contraseña.

  EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

Al igual que hemos usado vistas genericas para manejar el login y el logout del usuario, django nos proporciona herramientas predeterminadas

  from django.contrib.auth import views as auth_views

En el archivo urls.py le indicamos que use estas 4 urls
  /password_reset/: Donde el usuario ingresa su correo electrónico.
  /password_reset/done/: Mensaje de confirmación después de enviar el correo.
  /reset/<uidb64>/<token>/: Página para establecer una nueva contraseña.
  /reset/done/: Mensaje de éxito tras cambiar la contraseña.

El token es una "clave" que usa django internamente para asegurarse de la identificacion y de la validez de la solicitud de cambio de contraseña

En el template de login.html he creado con boostrap un pequeño div para que al usuario se le redirija a la url de recuperacion de contraseña 
<div id="centrado" style="display: flex;justify-content: center;align-items: center;">
    <div class="card text-center" style="width: 300px;">
        <div class="card-header h5 text-white bg-primary">Recuperar contraseña</div>
        <div class="card-body px-5">
            <p class="card-text py-2">
                Ingrese su email y sigue las instrucciones para recuperar su contraseña
            </p>
            <a href={% url 'password_reset' %} data-mdb-ripple-init class="btn btn-primary w-100">Resetear contraseña</a>
        </div>
    </div>
</div>


# Documentación de Permisos en la API

Esta API gestiona los permisos de acceso de los usuarios, los cuales pueden ser de tres tipos:

- **Admin**: Tiene acceso total a todas las funcionalidades.
- **Trabajador**: Tiene permisos específicos para gestionar inspecciones y facturas.
- **Cliente**: Tiene permisos para gestionar citas y vehículos.

## Tipo de Usuarios y Permisos

### 1. **Administrador** (Admin)

El **Administrador** tiene permisos completos para gestionar todos los aspectos de la API, incluyendo la creación, edición y eliminación de todos los modelos, así como la gestión de permisos y autenticación.

#### Permisos:
'ITV.view_local'
'ITV.view_cita'
'ITV.add_maquinaria'
'ITV.add_usuario'
'ITV.change_trabajador'
'ITV.add_cliente'
'ITV.change_usuario'
'ITV.add_vehiculo'
'ITV.view_vehiculo'
'ITV.change_local'
'ITV.delete_empresaexterna'
'ITV.view_usuario'
'ITV.add_inspeccion'
'ITV.change_empresaexterna'
'ITV.view_trabajador'
'ITV.change_maquinaria'
'ITV.change_estacionitv'
'ITV.add_cita'
'ITV.view_estacionitv'
'ITV.view_maquinaria'
'ITV.change_factura'
'ITV.add_empresaexterna'
'ITV.view_cliente'
'ITV.delete_vehiculo'
'ITV.add_local'
'ITV.add_estacionitv'
'ITV.view_empresaexterna'
'ITV.delete_estacionitv'
'ITV.delete_factura'
'ITV.add_trabajador'
'ITV.change_inspeccion'
'ITV.add_factura'
'ITV.change_cita'

### 2. **Trabajador** (Trabajador)

El **Trabajador** tiene permisos limitados para gestionar inspecciones y facturas. Este perfil no puede gestionar usuarios ni locales, pero sí puede cambiar la información relacionada con las inspecciones y las facturas.

#### Permisos:
'ITV.change_factura'
'ITV.add_inspeccion'
'ITV.view_factura'
'ITV.delete_inspeccion'
'ITV.delete_factura'
'ITV.view_inspeccion'
'ITV.change_inspeccion'
'ITV.add_factura'

### 3. **Cliente** (Cliente)

El **Cliente** tiene permisos para gestionar sus citas y vehículos. No tiene acceso a la administración de inscripciones ni a la edición de otros usuarios.

#### Permisos:
'ITV.view_cita'
'ITV.change_vehiculo'
'ITV.delete_vehiculo'
'ITV.delete_cita'
'ITV.add_cita'
'ITV.add_vehiculo'
'ITV.view_vehiculo'
'ITV.change_cita'