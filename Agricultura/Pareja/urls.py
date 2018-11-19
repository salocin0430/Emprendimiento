from django.urls import path
from .views import *

app_name = 'Pareja'
urlpatterns = [
	path('registrate/', Registro, name='registro'),
    #<int:user_id>/<int:boda_id>/<int:ceremonia_id>/ : Se debe llevar el url al de este estilo
    path('enamorado1/', Enamorado1, name='enamorado1'),
    path('enamorado2/', Enamorado2, name='enamorado2'),
    path('cerrar-sesion/', Logout, name='cerrar-sesion'),
]