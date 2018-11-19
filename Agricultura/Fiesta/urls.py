from django.urls import path
from .views import fiestaDashboardView

app_name = 'Fiesta'
urlpatterns = [
	path('<int:user_id>/<int:boda_id>/<int:fiesta_id>/', fiestaDashboardView , name='dashboard')
]