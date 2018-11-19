from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *
# Register your models here.
# LunaMiel

class ActividadAdmin(ModelAdmin):
    list_display = ('nombre','imagen','precio')

class HotelAdmin(ModelAdmin):
    list_display = ('nombre', 'imagen', 'precio')

admin.site.register(Plan)
admin.site.register(Actividad,ActividadAdmin)
admin.site.register(Hotel,HotelAdmin)
admin.site.register(ActividadPlan)
admin.site.register(HotelPlan)
admin.site.register(LunaMielEvento)
admin.site.register(ActividadCarrito)
admin.site.register(HotelCarrito)
