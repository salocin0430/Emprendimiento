from django.db import models
from Domain.models import *

# Create your models here.
# Validators
import re
from django.core.exceptions import ValidationError
TYPE=(
	('masculino','Masculino'),
	('femenino' ,'Femenino'),
	('mixto', 'Mixta')
	)

def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	#print("el valor de value[0] es %s -" % (value[0]))
	if result is not None:	
		if len(result.group(0))!=len(str(value)):
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		raise ValidationError('este campo debe ser solamente númerico')

#Pareja Models
		
class Enamorado(models.Model):
	User=models.OneToOneField(User, on_delete=models.CASCADE)
	cedula=models.CharField(max_length=50, validators=[numeric_validator])
	telefono=models.CharField(max_length=50, null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.User.first_name+" "+self.User.last_name+"-"+self.cedula+" -> Enamorado: {}".format(self.id)
		
class Belleza(models.Model):
	maquillaje=models.CharField(max_length=250)
	peinado=models.CharField(max_length=250)
	imagen=models.ImageField(upload_to="Pareja/Belleza", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.maquillaje+" <-> "+self.peinado+" -> Belleza: {}".format(self.id)

class BellezaCarrito(models.Model):
	Enamorado=models.ForeignKey(Enamorado, on_delete=models.CASCADE)
	Belleza=models.ForeignKey(Belleza, on_delete=models.CASCADE)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.Enamorado.__str__()+" <-> "+self.Belleza.__str__()+" -> Belleza Carrito: {}".format(self.id)
		
class Accesorio(models.Model):
	nombre=models.CharField(max_length=250)
	tipoObjeto=models.CharField(max_length=50)# Esto necesita un Choices
	alquilado=models.BooleanField(default=False)
	imagen=models.ImageField(upload_to="Pareja/Accesorio", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.nombre+" <-> "+self.tipoObjeto+" -> Alquilado: {} -> Accesorio: {}".format(self.alquilado, self.id)
		
class AccesorioCarrito(models.Model):
	Enamorado=models.ForeignKey(Enamorado, on_delete=models.CASCADE)
	Accesorio=models.ForeignKey(Accesorio, on_delete=models.CASCADE)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.Enamorado.__str__()+" <-> ".self.Accesorio.__str__()+" -> Accesorio Carrito: {}".format(self.id)
		
class Prenda(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	talla=models.CharField(max_length=250)
	imagen=models.ImageField(upload_to="Pareja/Prenda", null=True, blank=True, default=None)
	tipo = models.CharField(choices=TYPE, blank=True , default=None, max_length=50)
	precio=models.BigIntegerField(default=0)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.nombre+" -> Talla: {} -> tipo: {} -> Prenda: {}".format(self.talla, self.tipo, self.id)
		
class PrendaCarrito(models.Model):
	Enamorado=models.ForeignKey(Enamorado, on_delete=models.CASCADE)
	Prenda=models.ForeignKey(Prenda, on_delete=models.CASCADE)
	class Meta:
		app_label = 'Pareja'
	def __str__(self):
		return self.Enamorado.__str__()+" <-> "+self.Prenda.__str__()+" -> Prenda Carrito: {}".format(self.id)
