from django.urls import path

from .api_views import *

urlpatterns =[
    path('citas',cita_list)
]
