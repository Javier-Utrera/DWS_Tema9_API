from django.urls import path

from .api_views import *

urlpatterns =[
    #Listar-------------------
    path('clientes/listar_clientes',api_listar_clientes),
    path('citas/listar_citas',api_listar_citas),
]
