from django.urls import path
from .views import *

app_name = 'LunaMiel'
urlpatterns = [
    path('',dashboardView , name='dashboard'),
    path('actividades',post_actividad,name='anadir_actividad'),
    path('actividades/<int:id>',delete_actividad,name='borrar_actividad'),
    path('hoteles',post_hotel,name='anadir_hotel'),
    path('hoteles/<int:id>',delete_hotel,name='borrar_hotel'),
]