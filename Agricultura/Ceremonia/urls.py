from django.urls import path
from .views import *

app_name = 'Ceremonia'
urlpatterns = [
	
	path('<int:user_id>/<int:boda_id>/<int:ceremonia_id>/', ceremoniaDashboardView , name='dashboard')
	
]