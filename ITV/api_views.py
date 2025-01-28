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