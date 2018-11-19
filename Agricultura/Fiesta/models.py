from django.db import models
from Domain.models import *
# Create your models here.
# Fiesta Models

class FiestaEvento(models.Model):
	Boda=models.ForeignKey(Boda, on_delete=models.CASCADE)
	Lugar=models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, default=None)
	Fotos=models.BooleanField(blank=True, default=False)
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.Boda.__str__()+" -> Fiesta: {}".format(self.id)

class Alimento(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	imagen=models.ImageField(upload_to="Fiesta/Alimento", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)

	def __str__(self):
		return self.nombre+" -> Alimento: {}".format(self.id)
		
class AlimentoCarrito(models.Model):
	FiestaEvento=models.ForeignKey(FiestaEvento, on_delete=models.CASCADE)
	Alimento=models.ForeignKey(Alimento, on_delete=models.CASCADE)
	Cantidad = models.IntegerField(default=1)
	subtotal = models.BigIntegerField(default=0)
	def __str__(self):
		return self.FiestaEvento.__str__()+" <-> "+self.Alimento.__str__()+" -> Alimento carrito: {}".format(self.id)
		
class Entretenimiento(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	imagen=models.ImageField(upload_to="Fiesta/Entretenimiento", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)

	def __str__(self):
		return self.nombre+" -> Entretenimiento: {}".format(self.id)

class EntretenimientoCarrito(models.Model):
	FiestaEvento=models.ForeignKey(FiestaEvento, on_delete=models.CASCADE)
	Entretenimiento=models.ForeignKey(Entretenimiento, on_delete=models.CASCADE)
	def __str__(self):
		return self.FiestaEvento.__str__()+" <-> "+self.Entretenimiento.__str__()+" -> Entretenimiento Carrito: {}".format(self.id)

class DecoracionFiesta(models.Model):
	nombre=models.CharField(max_length=250, null=True, blank=True, default=None)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	imagen=models.ImageField(upload_to="Fiesta/Decoracion", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		verbose_name = "Decoración"
		verbose_name_plural = "Decoraciones"
	
	def __str__(self):
		return self.nombre+" -> Decoracion Fiesta: {}".format(self.id)

class DecoracionFiestaCarrito(models.Model):
	FiestaEvento=models.ForeignKey(FiestaEvento, on_delete=models.CASCADE)
	Decoracion=models.ForeignKey(DecoracionFiesta, on_delete=models.CASCADE)
	cantidad=models.IntegerField()
	def __str__(self):
		return self.FiestaEvento.__str__()+" <-> "+self.Decoracion.__str__()+" -> Decoracion Fiesta Carrito: {}".format(self.id)