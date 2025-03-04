from django.shortcuts import render
from .models import *
from .serializers import *
from .forms import * 
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group
import traceback

def api_errores(serializer, mensaje):
    if serializer.is_valid():
        try:
            serializer.save()
            return Response({"mensaje": mensaje}, status=status.HTTP_201_CREATED)  # ✅ Devuelve JSON válido
        
        except Exception as error:
            print("❌ ERROR 500 en la API:", repr(error))
            traceback.print_exc() 
            return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    else:
        print("🚨 ERRORES DEL SERIALIZADOR:", serializer.errors)
        return Response({"errores": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  # ✅ Estructura JSON correcta
    
def verificar_permiso(request, permiso):
    print(f"Usuario autenticado en la API: {request.user}")
    print(f"Permisos del usuario: {request.user.get_all_permissions()}")

    if not request.user.has_perm(permiso):
        return Response(
            {"error": "No tienes permisos para realizar esta acción."},
            status=status.HTTP_403_FORBIDDEN
        )
    return None          

#Listar--------------------------------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def api_listar_locales(request):
    permiso = verificar_permiso(request, "ITV.view_local")  
    if permiso:  
        return permiso
    locales = Local.objects.all()
    serializer = LocalSerializer(locales, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_clientes(request):
    permiso = verificar_permiso(request, "ITV.view_cliente")  
    if permiso:  
        return permiso 
    clientes = Cliente.objects.prefetch_related('cliente_cita').all() 
    serializer=ClienteSerializerCompleto(clientes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_citas(request):
    permiso = verificar_permiso(request, "ITV.view_cita")  
    if permiso:  
        return permiso 
    citas = Cita.objects.select_related("cliente", "estacion").all()
    serializer=CitaSerializer(citas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_trabajadores(request):
    permiso = verificar_permiso(request, "ITV.view_trabajador")  
    if permiso:  
        return permiso 
    trabajadores=Trabajador.objects.prefetch_related("estacion",
                                                     Prefetch("trabajador_Inspeccion"),
                                                     Prefetch("trabajador_Vehiculo")).all()
    serializer=TrabajadorSerializer(trabajadores,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_vehiculos(request):
    permiso = verificar_permiso(request, "ITV.view_vehiculo")  
    if permiso:  
        return permiso 
    vehiculos=Vehiculo.objects.select_related("propietario").prefetch_related("trabajadores",Prefetch("vehiculo_Inspeccion")).all()
    serializer=VehiculoSerializerCompleto(vehiculos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_inspecciones(request):
    permiso = verificar_permiso(request, "ITV.view_inspeccion")  
    if permiso:  
        return permiso 
    inspecciones=Inspeccion.objects.select_related("trabajador","vehiculo").prefetch_related(Prefetch("inspeccion_Factura")).all()
    serializer=InspeccionSerializer(inspecciones,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_estaciones(request):
    permiso = verificar_permiso(request, "ITV.view_estacionitv")  
    if permiso:  
        return permiso 
    estaciones=EstacionItv.objects.select_related("local").all()
    serializer=EstacionSerializer(estaciones,many=True)
    return Response(serializer.data)

#Obtener-----------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET']) 
def api_cita_obtener(request,cita_id):
    cita = Cita.objects.select_related("cliente", "estacion")
    cita = cita.get(id=cita_id)
    serializer = CitaSerializer(cita)
    return Response(serializer.data)

@api_view(['GET'])
def api_local_obtener(request, local_id):
    local = Local.objects.get(id=local_id)
    serializer = LocalSerializer(local)
    return Response(serializer.data)


@api_view(['GET'])
def api_trabajador_obtener(request, trabajador_id):
    trabajador = Trabajador.objects.prefetch_related("estacion").get(id=trabajador_id)
    serializer = TrabajadorSerializer(trabajador)
    return Response(serializer.data)

@api_view(['GET'])
def api_obtener_vehiculo(request, vehiculo_id):
    vehiculo = Vehiculo.objects.select_related("propietario").prefetch_related("trabajadores", Prefetch("vehiculo_Inspeccion")).get(id=vehiculo_id)
    serializer = VehiculoSerializerCompleto(vehiculo)
    return Response(serializer.data)
#Buscar-----------------------------------------------------------------------------------------------------------------------------------
@api_view(['GET'])
def api_buscar_local(request):
    permiso = verificar_permiso(request, "ITV.view_local")  
    if permiso:  
        return permiso 
    if len(request.query_params) > 0:
        formulario = BusquedaAvanzadaLocal(request.GET)
        
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            QSlocales = Local.objects.all()
            
            precio_v = formulario.cleaned_data.get("precio")
            metros_v = formulario.cleaned_data.get("metros")
            duenio_v = formulario.cleaned_data.get("duenio")

            if precio_v is not None:
                QSlocales = QSlocales.filter(precio__lte=precio_v)
                mensaje += f"Precio máximo buscado: {precio_v}\n"
            if metros_v is not None:
                QSlocales = QSlocales.filter(metros__gte=metros_v)
                mensaje += f"Metros mínimos buscados: {metros_v}\n"
            if duenio_v:
                QSlocales = QSlocales.filter(duenio__icontains=duenio_v)
                mensaje += f"Dueño buscado: {duenio_v}\n"
            
            locales = QSlocales.all()
            serializer = LocalSerializer(locales, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_buscar_cita(request):
    permiso = verificar_permiso(request, "ITV.view_cita")  
    if permiso:  
        return permiso 
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaCita(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            QScitas = Cita.objects.select_related("cliente", "estacion")
            
            matriculav = formulario.cleaned_data.get("matricula")
            tipo_inspeccionv = formulario.cleaned_data.get("tipo_inspeccion")
            fecha_propuestav = formulario.cleaned_data.get("fecha_propuesta")
            
            
            if matriculav != "":
                QScitas = QScitas.filter(matricula__icontains=matriculav)
                mensaje += "Matrícula buscada: {matriculav}\n"
            if tipo_inspeccionv != "":
                QScitas = QScitas.filter(tipo_inspeccion=tipo_inspeccionv)
                mensaje += "Tipo de inspección buscado: {tipo_inspeccionv}\n"
            if fecha_propuestav is not None:
                QScitas = QScitas.filter(fecha_propuesta=fecha_propuestav)
                mensaje += "Fecha propuesta buscada: {fecha_propuestav.strftime('%d-%m-%Y')}\n"
            
            citas=QScitas.all()
            serializer=CitaSerializer(citas,many=True)     
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def api_buscar_inspeccion(request):
    permiso = verificar_permiso(request, "ITV.view_inspeccion")  
    if permiso:  
        return permiso 
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaInspeccion(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            QSinspecciones = Inspeccion.objects.select_related("trabajador","vehiculo").prefetch_related(Prefetch("inspeccion_Factura"))
            
            resultado_inspeccionv=formulario.cleaned_data.get("resultado_inspeccion")         
            notas_inspeccionv=formulario.cleaned_data.get("notas_inspeccion") 
            fecha_inspeccionv=formulario.cleaned_data.get("fecha_inspeccion") 
            
            
            if(resultado_inspeccionv !=""):
                QSinspecciones = QSinspecciones.filter(resultado_inspeccion__contains=resultado_inspeccionv)
                mensaje+="Texto que se ha buscado " + resultado_inspeccionv  +"\n"
            if(notas_inspeccionv!=""):
                QSinspecciones=QSinspecciones.filter(notas_inspeccion__contains=notas_inspeccionv)
                mensaje+="Texto de la inspeccion por el que se ha buscado " + notas_inspeccionv + "\n"
            if(not fecha_inspeccionv is None):
                QSinspecciones=QSinspecciones.filter(fecha_inspeccion__gte=fecha_inspeccionv)
                mensaje+="La fecha por la que se esta buscando es" + datetime.strftime(fecha_inspeccionv,'%d-%m-%Y')+"\n"
            
            inspecciones=QSinspecciones.all()
            serializer=InspeccionSerializer(inspecciones,many=True)     
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def api_buscar_vehiculo(request):
    permiso = verificar_permiso(request, "ITV.view_vehiculo")  
    if permiso:  
        return permiso 
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaVehiculo(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            QSvehiculos=Vehiculo.objects.select_related("propietario").prefetch_related("trabajadores",Prefetch("vehiculo_Inspeccion"))
            
            marcav=formulario.cleaned_data.get("marca")
            potenciav=formulario.cleaned_data.get("potencia") 
            matriculav=formulario.cleaned_data.get("matricula") 
            
            
            if(marcav != ""):
                QSvehiculos=QSvehiculos.filter(marca__icontains=marcav)
                mensaje+="Marca que se ha buscado " + marcav  +"\n"
            if(potenciav is not None):
                QSvehiculos=QSvehiculos.filter(potencia=potenciav)
                mensaje+="Inspeccion por el que se ha buscado " + str(potenciav) + "\n"
            if(matriculav!= ""):
                QSvehiculos=QSvehiculos.filter(matricula__contains=matriculav)
                mensaje+="Matricula que se esta buscando es" + matriculav +"\n"
            
            vehiculos=QSvehiculos.all()
            serializer=VehiculoSerializer(vehiculos,many=True)     
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def api_buscar_trabajador(request):
    permiso = verificar_permiso(request, "ITV.view_trabajador")  
    if permiso:  
        return permiso 
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaTrabajador(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            trabajadores=Trabajador.objects.prefetch_related("estacion",
                                                     Prefetch("trabajador_Inspeccion"),
                                                     Prefetch("trabajador_Vehiculo"))
            
            nombrev=formulario.cleaned_data.get("nombre")
            sueldov=formulario.cleaned_data.get("sueldo") 
            puestov=formulario.cleaned_data.get("puesto") 
            
            
            if(nombrev != ""):
                trabajadores=trabajadores.filter(nombre__contains=nombrev)
                mensaje+="Texto que se ha buscado " + nombrev  +"\n"
            if(not sueldov is None):
                trabajadores=trabajadores.filter(sueldo=sueldov)
                mensaje+="Sueldo que se ha buscado " + str(sueldov) + "\n"
            if(puestov != ""):
                trabajadores=trabajadores.filter(puesto=puestov)
                mensaje+="Puesto que se esta buscando es" +  puestov+"\n"
            
            trabajadores=trabajadores.all()
            serializer=TrabajadorSoloSerializer(trabajadores,many=True)     
            return Response(serializer.data)
        else:
            return Response(formulario.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({},status=status.HTTP_400_BAD_REQUEST)
    
#POST-----------------------------------------------------------------------------------------------------------------------------------
@api_view(['POST'])
def api_crear_local(request):
    permiso = verificar_permiso(request, "ITV.add_local")  
    if permiso:  
        return permiso 
    print(request.data)
    localSerializer = LocalSerializerCreate(data=request.data)
    return api_errores(localSerializer, "Local CREADO")

@api_view(['POST'])
def api_crear_cita(request):
    permiso = verificar_permiso(request, "ITV.add_cita")  
    if permiso:  
        return permiso
    print(request.data)
    citaSerializerCreate = CitaSerializerCreate(data=request.data)
    return api_errores(citaSerializerCreate,"Cita CREADA")

@api_view(['POST'])
def api_crear_trabajador(request):
    permiso = verificar_permiso(request, "ITV.add_trabajador")  
    if permiso:  
        return permiso
    serializer = TrabajadorSerializerCreate(data=request.data)
    return api_errores(serializer, "Trabajador CREADO")

@api_view(['POST'])
def api_crear_vehiculo(request):
    permiso = verificar_permiso(request, "ITV.add_vehiculo")  
    if permiso:  
        return permiso
    print("📌 JSON recibido en la API:", request.data)  

    serializer = VehiculoSerializerCreate(data=request.data)
    return api_errores(serializer, "Vehículo CREADO")
    
#PUT---------------------------------------------------------------------------------------------------------------------------------------
@api_view(['PUT'])
def api_editar_local(request, local_id):
    permiso = verificar_permiso(request, "ITV.change_local")  
    if permiso:  
        return permiso
    local = Local.objects.get(id=local_id)
    localSerializer = LocalSerializerCreate(data=request.data, instance=local)
    return api_errores(localSerializer, "Local EDITADO")

@api_view(['PUT'])
def api_editar_cita(request, cita_id):
    permiso = verificar_permiso(request, "ITV.change_cita")  
    if permiso:  
        return permiso
    cita = Cita.objects.get(id=cita_id)
    print("📌 JSON recibido en la API (PUT):", request.data)
    serializer = CitaSerializerCreate(data=request.data, instance=cita)
    if not serializer.is_valid():
        print("🚨 Errores en el serializador:", serializer.errors)
    serializer.save()
    return api_errores(serializer, "Cita EDITADA")

@api_view(['PUT'])
def api_editar_trabajador(request, trabajador_id):
    permiso = verificar_permiso(request, "ITV.change_trabajdor")  
    if permiso:  
        return permiso
    trabajador = Trabajador.objects.get(id=trabajador_id)
    serializer = TrabajadorSerializerCreate(data=request.data, instance=trabajador)
    return api_errores(serializer, "Trabajador EDITADO")

@api_view(['PUT'])
def api_editar_vehiculo(request, vehiculo_id):
    permiso = verificar_permiso(request, "ITV.change_vehiculo")  
    if permiso:  
        return permiso
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    print("📌 JSON recibido en la API (PUT):", request.data)
    serializer = VehiculoSerializerCreate(data=request.data, instance=vehiculo)
    return api_errores(serializer, "Vehículo EDITADO")

#PATCH----------------------------------------------------------------------------------------------------------------------------------------
@api_view(['PATCH'])
def api_actualizar_local_duenio(request, local_id):
    permiso = verificar_permiso(request, "ITV.change_local")  
    if permiso:  
        return permiso
    local = Local.objects.get(id=local_id)
    serializer = LocalSerializerActualizarDuenio(data=request.data, instance=local)
    return api_errores(serializer, "Dueño del local EDITADO")

@api_view(['PATCH'])
def api_actualizar_cita_matricula(request,cita_id):
    permiso = verificar_permiso(request, "ITV.change_cita")  
    if permiso:  
        return permiso
    cita=Cita.objects.get(id=cita_id)
    serializers = CitaSerializerActualizarMatricula(data=request.data, instance = cita)
    return api_errores(serializers,"Matricula de la cita EDITADA")

@api_view(['PATCH'])
def api_actualizar_trabajador_puesto(request, trabajador_id):
    permiso = verificar_permiso(request, "ITV.change_trabajdor")  
    if permiso:  
        return permiso
    trabajador = Trabajador.objects.get(id=trabajador_id)
    serializer = TrabajadorSerializerActualizarPuesto(data=request.data, instance=trabajador)
    return api_errores(serializer, "Puesto del Trabajador EDITADO")

@api_view(['PATCH'])
def api_actualizar_vehiculo_matricula(request, vehiculo_id):
    permiso = verificar_permiso(request, "ITV.change_vehiculo")  
    if permiso:  
        return permiso
    print(f"ID del vehículo recibido: {vehiculo_id}") 
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    serializer = VehiculoSerializerActualizarMatricula(data=request.data, instance=vehiculo)
    return api_errores(serializer, "Matrícula del Vehículo ACTUALIZADA")
#DELETE----------------------------------------------------------------------------------------------------------------------------------------
@api_view(['DELETE'])
def api_eliminar_local(request, local_id):
    permiso = verificar_permiso(request, "ITV.delete_local")  
    if permiso:  
        return permiso
    local = Local.objects.get(id=local_id)
    try:
        local.delete()
        return Response("Local eliminado correctamente")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def api_eliminar_cita(request,cita_id):
    permiso = verificar_permiso(request, "ITV.delete_cita")  
    if permiso:  
        return permiso
    cita=Cita.objects.get(id=cita_id)
    try:
        cita.delete()
        return Response("Cita eliminada correctamente")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def api_eliminar_trabajador(request, trabajador_id):
    permiso = verificar_permiso(request, "ITV.delete_trabajador")  
    if permiso:  
        return permiso
    trabajador = Trabajador.objects.get(id=trabajador_id)
    try:
        trabajador.delete()
        return Response("Trabajador eliminado correctamente")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['DELETE'])
def api_eliminar_vehiculo(request, vehiculo_id):
    permiso = verificar_permiso(request, "ITV.delete_vehiculo")  
    if permiso:  
        return permiso
    vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    try:
        vehiculo.delete()
        return Response("Vehículo eliminado correctamente")
    except Exception as error:
        return Response(str(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
#ViewSet------------------
class LocalViewSet(viewsets.ModelViewSet):
    
    queryset = Local.objects.all()

    def get_serializer_class(self):
        # Para las acciones de creación y actualización usamos el serializer con validaciones
        if self.action in ['create', 'update', 'partial_update']:
            return LocalSerializerCreate
        # Para listar y obtener usamos el serializer completo
        return LocalSerializer
    
    
class api_registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        
        print("Datos Recibidos:", request.data)  
        
        if not serializers.is_valid():  
            print("Errores en el serializer:", serializers.errors)  
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if serializers.is_valid():
            try:
                rol= int(request.data.get('rol'))

                user = Usuario.objects.create_user(
                        username=serializers.validated_data.get("username"), 
                        email=serializers.validated_data.get("email"), 
                        password=serializers.validated_data.get("password1"),
                        rol=rol,
                )
                user.save()

                if rol == Usuario.CLIENTE:
                    grupo = Group.objects.get(name='Clientes')
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create(
                        usuario=user,
                        nombre=serializers.validated_data.get("username"),
                        email=serializers.validated_data.get("email"),
                        fecha_nacimiento=serializers.validated_data.get("fecha_nacimiento"),
                        apellidos=serializers.validated_data.get("apellidos"),
                        dni=serializers.validated_data.get("dni")
                    )
                    cliente.save()

                elif rol == Usuario.TRABAJADOR:
                    grupo = Group.objects.get(name='Trabajadores')
                    grupo.user_set.add(user)
                    trabajador = Trabajador.objects.create(
                        usuario=user,
                        email=serializers.validated_data.get("email"),
                        nombre=serializers.validated_data.get("username"),
                        puesto=serializers.validated_data.get("puesto")
                    )
                    trabajador.save()

                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)

            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        
from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_citas_cliente(request):
    permiso = verificar_permiso(request, "ITV.view_cita")  
    if permiso:  
        return permiso
    try:
        usuario = request.user
        rol= int(usuario.rol)
        if rol == Usuario.ADMINISTRADOR:  
            citas = Cita.objects.all()  
        else:
            cliente = Cliente.objects.filter(usuario=usuario).first()  
            citas = Cita.objects.filter(cliente=cliente)
        serializer = CitaSerializer(citas, many=True)
        return Response(serializer.data)
    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])   
def api_listar_vehiculos_cliente(request):
    permiso = verificar_permiso(request, "ITV.view_vehiculo")  
    if permiso:  
        return permiso
    try:
        usuario = request.user  
        rol= int(usuario.rol)
        if rol == Usuario.ADMINISTRADOR:  
            vehiculos = Vehiculo.objects.all()
        else:
            cliente = Cliente.objects.filter(usuario=usuario).first()  
            vehiculos = Vehiculo.objects.filter(propietario=cliente)

        serializer = VehiculoSerializer(vehiculos, many=True)
        return Response(serializer.data)

    except Exception as error:
        return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(["POST"])    
def api_crear_cita_cliente(request):
    try:
        usuario = request.user
        cliente = Cliente.objects.filter(usuario=usuario).first()

        if not cliente:
            return Response({"error": "No eres un cliente registrado."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data["cliente"] = cliente.id

        serializer = CitaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def api_crear_vehiculo_cliente(request):
    try:
        usuario = request.user
        cliente = Cliente.objects.filter(usuario=usuario).first()

        if not cliente:
            return Response({"error": "No eres un cliente registrado."}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data["propietario"] = cliente.id

        serializer = VehiculoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)