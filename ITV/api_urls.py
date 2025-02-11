from django.urls import path

from .api_views import *

urlpatterns =[
    #Listar-------------------
    path('clientes/listar_clientes',api_listar_clientes),
    path('citas/listar_citas',api_listar_citas),
    path('trabajadores/listar_trabajadores',api_listar_trabajadores),
    path('vehiculos/listar_vehiculos',api_listar_vehiculos),
    path('inspecciones/listar_inspecciones',api_listar_inspecciones),
    path('estaciones/listar_estaciones',api_listar_estaciones),
    
    path('citas/buscar',api_buscar_cita),
    path('inspecciones/buscar',api_buscar_inspeccion),
    path('vehiculos/buscar',api_buscar_vehiculo),
    path('trabajadores/buscar',api_buscar_trabajador),
    
    path('citas/crear',api_crear_cita)
]
