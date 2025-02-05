from django.shortcuts import render
from .models import *
from .serializers import *
from .forms import * 
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

#Listar---------------------------------------------------------
@api_view(['GET'])
def api_listar_clientes(request):
    clientes = Cliente.objects.prefetch_related('cliente_cita').all() 
    serializer=ClienteSerializerCompleto(clientes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_citas(request):
    citas = Cita.objects.select_related("cliente", "estacion").all()
    serializer=CitaSerializer(citas,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_trabajadores(request):
    trabajadores=Trabajador.objects.prefetch_related("estacion",
                                                     Prefetch("trabajador_Inspeccion"),
                                                     Prefetch("trabajador_Vehiculo")).all()
    serializer=TrabajadorSerializer(trabajadores,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_vehiculos(request):
    vehiculos=Vehiculo.objects.select_related("propietario").prefetch_related("trabajadores",Prefetch("vehiculo_Inspeccion")).all()
    serializer=TrabajadorSerializer(vehiculos,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_listar_inspecciones(request):
    inspecciones=Inspeccion.objects.select_related("trabajador","vehiculo").prefetch_related(Prefetch("inspeccion_Factura")).all()
    serializer=InspeccionSerializer(inspecciones,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def api_buscar_cita(request):
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
                QSinspecciones=QSinspecciones.filter(fecha_inspeccion=fecha_inspeccionv)
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
    if (len(request.query_params) > 0):
        formulario = BusquedaAvanzadaVehiculo(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            QSvehiculos=Vehiculo.objects.select_related("propietario").prefetch_related("trabajadores",Prefetch("vehiculo_Inspeccion"))
            
            marcav=formulario.cleaned_data.get("marca")
            potenciav=formulario.cleaned_data.get("potencia") 
            matriculav=formulario.cleaned_data.get("matricula") 
            
            
            if(marcav != ""):
                QSvehiculos=QSvehiculos.filter(marca=marcav)
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