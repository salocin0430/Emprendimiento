"""BodaKaoz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Pareja.views import Login, TableroResumen

from django.conf import settings
from BodaKaoz.views import *
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	# path('', include('Domain.urls')), #contenedor de urls principal
	path('', Login , name='index' ),
	path('resumen/', TableroResumen, name='tableroResumen'),# Tablero temporal hecho por pareja
	path('pareja/', include('Pareja.urls', namespace="Pareja")),
	path('Ceremonia/', include('Ceremonia.urls', namespace="Ceremonia")),
	path('fiesta/', include('Fiesta.urls', namespace="Fiesta")),
	path('LunaMiel/', include('LunaMiel.urls', namespace="LunaMiel")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404View
handler500 = handler404View
handler403 = handler404View
handler400 = handler404View
