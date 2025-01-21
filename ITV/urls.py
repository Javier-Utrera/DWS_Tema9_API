from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from .import views

urlpatterns = [
    path('', views.index,name="urls_index"),
    #1
    path('clientes/listar_clientes', views.listar_clientes,name="listar_clientes"),
    
    #2
    path('citas/listar_citas', views.listar_citas,name="listar_citas"),
    
    #3
    path('estaciones/listar_estaciones', views.listar_estaciones,name="listar_estaciones"),
    
    #4
    path('trabajadores/listar_trabajadores', views.listar_trabajadores,name="listar_trabajadores"),
    
    #5
    path('inspecciones/listar_inspecciones', views.listar_inspecciones,name="listar_inspecciones"),
     
    #7
    path('vehiculos/listar_vehiculos', views.listar_vehiculos,name="listar_vehiculos"),
    
    #8
    path('locales/listar_locales', views.listar_locales,name="listar_locales"),
    
    
    #FOMULARIOS
    
        #CREATE

    #Crear cliente
    path('clientes/create', views.procesar_cliente,name="procesar_cliente"),
    
    #Crear inspeccion
    path('inspecciones/create', views.procesar_inspeccion,name="procesar_inspeccion"),
    
    #Crear vehiculo
    path('vehiculos/create', views.procesar_vehiculo,name="procesar_vehiculo"),
    
    #Crear local
    path('locales/create', views.procesar_local,name="procesar_local"),
    
    #Crear estacion
    path('estaciones/create', views.procesar_estacion,name="procesar_estacion"),
    
    #Crear trabajador
    path('trabajadores/create', views.procesar_trabajador,name="procesar_trabajador"),

    #Crear cita
    path('citas/create', views.procesar_cita,name="procesar_cita"),
    
        #BUSQUEDA AVANZADA
        
    #Buscar cliente   
    path('clientes/buscar',views.buscar_cliente,name="buscar_cliente"),
    
    #Buscar inspeccion
    path('inspecciones/buscar',views.buscar_inspeccion,name="buscar_inspeccion"),
    
    #Buscar vehiculo 
    path('vehiculos/buscar',views.buscar_vehiculo,name="buscar_vehiculo"),
    
    #Buscar local
    path('locales/buscar',views.buscar_local,name="buscar_local"), 
    
    #Buscar estacion 
    path('estaciones/buscar',views.buscar_estacion,name="buscar_estacion"),
    
    #Buscar trabajador  
    path('trabajadores/buscar',views.buscar_trabajador,name="buscar_trabajador"),

    #Buscar cita  
    path('citas/buscar',views.buscar_cita,name="buscar_cita"),
    
        #ACTUALIZAR
    
    #Actualizar cliente
    path('clientes/editar/<int:cliente_id>', views.editar_cliente,name="editar_cliente"),
    
    #Actualizar inspeccion
    path('inspecciones/editar/<int:inspeccion_id>', views.editar_inspeccion,name="editar_inspeccion"),
    
    #Actualizar vehiculo
    path('vehiculos/editar/<int:vehiculo_id>', views.editar_vehiculo,name="editar_vehiculo"),
    
    #Actualizar local
    path('locales/editar/<int:local_id>', views.editar_local,name="editar_local"),
    
    #Actualizar estacion
    path('estaciones/editar/<int:estacion_id>', views.editar_estacion,name="editar_estacion"),
    
    #Actualizar trabajador
    path('trabajadores/editar/<int:trabajador_id>', views.editar_trabajador,name="editar_trabajador"),
    
    #Actualizar cita
    path('citas/editar/<int:cita_id>', views.editar_cita,name="editar_cita"),
    
        #Eliminar
        
    #Eliminar cliente    
    path('clientes/eliminar/<int:cliente_id>',views.eliminar_cliente,name='eliminar_cliente'),
    
    #Eliminar inspeccion    
    path('inspecciones/eliminar/<int:inspeccion_id>',views.eliminar_inspeccion,name='eliminar_inspeccion'),
    
    #Eliminar vehiculo    
    path('vehiculos/eliminar/<int:vehiculo_id>',views.eliminar_vehiculo,name='eliminar_vehiculo'),
    
    #Eliminar local    
    path('locales/eliminar/<int:local_id>',views.eliminar_local,name='eliminar_local'),
    
    #Eliminar estacion    
    path('estaciones/eliminar/<int:estacion_id>',views.eliminar_estacion,name='eliminar_estacion'),
    
    #Eliminar trabajador    
    path('trabajadores/eliminar/<int:trabajador_id>',views.eliminar_trabajador,name='eliminar_trabajador'),
    
    #Eliminar cita   
    path('citas/eliminar/<int:cita_id>',views.eliminar_cita,name='eliminar_cita'),
    
        #Registro
        
    #Registrar Usuario
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    
    #Recuperacion de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]       