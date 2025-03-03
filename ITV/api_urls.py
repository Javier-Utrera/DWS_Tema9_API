from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .api_views import *
#He visto que si uso este componente creo automaticamente las urls para el viewset que he creado, asi que la
#instancio en la variable router y me registra las urls del crud, osea estas (list, create, retrieve, update, partial_update y destroy).
router = DefaultRouter()
#todas las urls van a empezar por locales
router.register(r'locales', LocalViewSet, basename='local')

urlpatterns =[
    #aqui incluyo mis urls creadas automaticas ahi arriba en las rutas de mi aplicacion
    path('', include(router.urls)),
    #Listar-------------------
    path('clientes/listar_clientes',api_listar_clientes),
    path('inspecciones/listar_inspecciones',api_listar_inspecciones),
    path('inspecciones/buscar',api_buscar_inspeccion),
    path('estaciones/listar_estaciones',api_listar_estaciones),
      
    
    path('citas/listar_citas',api_listar_citas),
    path('citas/buscar',api_buscar_cita),
    path('citas/cita/<int:cita_id>',api_cita_obtener),    
    path('citas/crear',api_crear_cita),
    path('citas/editar/<int:cita_id>',api_editar_cita),
    path('citas/actualizar/matricula/<int:cita_id>',api_actualizar_cita_matricula),
    path('citas/eliminar/<int:cita_id>',api_eliminar_cita),
    
    
    path('locales/listar_locales', api_listar_locales),
    path('locales/buscar', api_buscar_local),
    path('locales/local/<int:local_id>', api_local_obtener),
    path('locales/crear', api_crear_local),
    path('locales/editar/<int:local_id>', api_editar_local),
    path('locales/actualizar/duenio/<int:local_id>', api_actualizar_local_duenio),
    path('locales/eliminar/<int:local_id>', api_eliminar_local), 
    
    
    path('trabajadores/listar_trabajadores',api_listar_trabajadores),
    path('trabajadores/buscar',api_buscar_trabajador),
    path('trabajadores/trabajador/<int:trabajador_id>', api_trabajador_obtener),
    path('trabajadores/crear', api_crear_trabajador),
    path('trabajadores/editar/<int:trabajador_id>', api_editar_trabajador),
    path('trabajadores/actualizar/puesto/<int:trabajador_id>', api_actualizar_trabajador_puesto),
    path('trabajadores/eliminar/<int:trabajador_id>', api_eliminar_trabajador),
    

    path('vehiculos/listar_vehiculos',api_listar_vehiculos),
    path('vehiculos/buscar',api_buscar_vehiculo),
    path('vehiculos/vehiculo/<int:vehiculo_id>', api_obtener_vehiculo),
    path('vehiculos/crear', api_crear_vehiculo),
    path('vehiculos/editar/<int:vehiculo_id>', api_editar_vehiculo),
    path('vehiculos/actualizar/matricula/<int:vehiculo_id>', api_actualizar_vehiculo_matricula),
    path('vehiculos/eliminar/<int:vehiculo_id>', api_eliminar_vehiculo),
    
    path('registrar/usuario',api_registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token),
    
    path('vehiculos/listar_vehiculos_cliente',api_listar_vehiculos_cliente),
    path('citas/listar_citas_cliente',api_listar_citas_cliente),
    
    path('citas/crear_cliente', api_crear_cita_cliente, name="api_crear_cita_cliente"),
    path('vehiculos/crear_cliente', api_crear_vehiculo_cliente, name="api_crear_vehiculo_cliente"),    
]
