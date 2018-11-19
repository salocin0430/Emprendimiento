from django.db import models
from django.contrib.auth.models import User
from Pareja.models import *

# Validators
import re
from django.core.exceptions import ValidationError


TYPE = (
    ('ceremonia','Ceremonia'),
    ('fiesta', 'Fiesta')
)



def numeric_validator(value):
	result=re.match('[0-9]*', str(value))
	#print("el valor de value[0] es %s -" % (value[0]))
	if result is not None:	
		if len(result.group(0))!=len(str(value)):
			raise ValidationError('este campo debe ser solamente númerico')
	else:
		raise ValidationError('este campo debe ser solamente númerico')


	
class Lugar(models.Model):
	nombre=models.CharField(max_length=250)
	direccion=models.CharField(max_length=250)
	capacidad=models.IntegerField()
	imagen=models.ImageField(upload_to="Domain/Lugar",null=True, blank=True, default=None)
	tipo = models.CharField(choices=TYPE, max_length=50 , default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		verbose_name = "Lugar"
		verbose_name_plural = "Lugares"
	
	def __str__(self):
		return self.nombre+" <-> "+self.tipo+" -> Lugar: {}".format(self.id)
		
		
# Clases de agrupamiento final
	
class Boda(models.Model):
	Enamorado1=models.ForeignKey(Enamorado, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='Enamorado1')
	Enamorado2=models.ForeignKey(Enamorado, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name='Enamorado2')
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.Enamorado1.__str__()+" <-> "+self.Enamorado2.__str__()+" -> Boda: {}".format(self.id)
	
class Transporte(models.Model):
	nombre=models.CharField(max_length=50)
	tipo=models.CharField(max_length=50)
	precio=models.BigIntegerField(default=0)
	
class TransporteCarrito(models.Model):
	Transporte=models.ForeignKey(Transporte, on_delete=models.CASCADE)
	Boda=models.ForeignKey(Boda, on_delete=models.CASCADE)
		

		

		

	


	