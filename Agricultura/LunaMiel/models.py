from django.db import models
from Domain.models import *
# Create your models here.
# LunaMiel - Models


class Plan(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	class Meta:
		verbose_name = "Plan"
		verbose_name_plural = "Planes"


class Actividad(models.Model):
	nombre=models.CharField(max_length=250)
	imagen=models.ImageField(null=True, blank=True, default=None, upload_to="LunaMiel/Actividad")
	precio=models.BigIntegerField(default=0)
	class Meta:
		verbose_name = "Actividad"
		verbose_name_plural = "Actividades"
	def __str__(self):
		return self.nombre

class Hotel(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	calificacion=models.IntegerField()
	imagen=models.ImageField(null=True, blank=True, default=None, upload_to="LunaMiel/Hotel")
	precio=models.BigIntegerField(default=0)
	
	class Meta:
		verbose_name = "Hotel"
		verbose_name_plural = "Hoteles"
	def __str__(self):
		return self.nombre


class ActividadPlan(models.Model):
	Plan=models.ForeignKey(Plan, on_delete=models.CASCADE)
	Actividad=models.ForeignKey(Actividad, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)
	class Meta:
		verbose_name = "Actividad plan"
		verbose_name_plural = "Actividad planes"


class HotelPlan(models.Model):
	Plan=models.ForeignKey(Plan, on_delete=models.CASCADE)
	Hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)
	class Meta:
		verbose_name = "Hotel plan"
		verbose_name_plural = "Hotel planes"


class LunaMielEvento(models.Model):
	Boda=models.ForeignKey(Boda, on_delete=models.CASCADE)
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.Boda.__str__()+" -> LunaMiel: {}".format(self.id)

class ActividadCarrito(models.Model):
	LunaMielEvento=models.ForeignKey(LunaMielEvento, on_delete=models.CASCADE)
	Actividad=models.ForeignKey(Actividad, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)
	def __str__(self):
		return self.LunaMielEvento.__str__()+" <-> Actividad: {}".format(self.Actividad.__str__())

	def total(self):
		return self.Actividad.precio*self.cantidad


class HotelCarrito(models.Model):
	Hotel=models.ForeignKey(Hotel, on_delete=models.CASCADE)
	LunaMielEvento=models.ForeignKey(LunaMielEvento, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)
	def __str__(self):
		return self.LunaMielEvento.__str__()+" <-> Hotel: {}".format(self.Hotel.__str__())
	def total(self):
		return self.Hotel.precio*self.cantidad