from django.shortcuts import render
from .models import *
from .serializers import *
from .forms import * 
from django.db.models import Prefetch
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
def buscar_cita(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaCita(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
                        
            matriculav = formulario.cleaned_data.get("matricula")
            tipo_inspeccionv = formulario.cleaned_data.get("tipo_inspeccion")
            fecha_propuestav = formulario.cleaned_data.get("fecha_propuesta")
                      
            if matriculav != "":
                citas = citas.filter(matricula__icontains=matriculav)
                mensaje += "Matrícula buscada: {matriculav}\n"
            if tipo_inspeccionv != "":
                citas = citas.filter(tipo_inspeccion=tipo_inspeccionv)
                mensaje += "Tipo de inspección buscado: {tipo_inspeccionv}\n"
            if fecha_propuestav is not None:
                citas = citas.filter(fecha_propuesta=fecha_propuestav)
                mensaje += "Fecha propuesta buscada: {fecha_propuestav.strftime('%d-%m-%Y')}\n"
                     
            return render(request, "citas/listar_citas.html", {
                "views_citas": citas,
                "texto_busqueda": mensaje,
            })
    else:
        formulario = BusquedaAvanzadaCita(None)
   
    return render(request, 'citas/busqueda_avanzada.html', {"formulario": formulario})
