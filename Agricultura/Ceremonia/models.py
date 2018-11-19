from django.db import models
from Domain.models import *

# Create your models here.
# Ceremonia Models


TYPE = (
    ('catolica','Catolica'),
    ('civil', 'Civil')
)

	
class Ministro(models.Model):
	nombre=models.CharField(max_length=250)
	tipo=models.CharField(choices=TYPE, max_length=50)
	imagen=models.ImageField(upload_to="Ceremonia/Ministro", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.nombre+" -> Ministro: {}".format(self.id)
		
class Musica(models.Model):
	nombre=models.CharField(max_length=250)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	imagen=models.ImageField(upload_to="Ceremonia/Musica", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.nombre+" -> Musica: {}".format(self.id)
		
class CeremoniaEvento(models.Model):
	Boda=models.ForeignKey(Boda, on_delete=models.CASCADE)
	Lugar=models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True, default=None)
	Ministro=models.ForeignKey(Ministro, on_delete=models.SET_NULL, null=True, blank=True, default=None)
	Musica=models.ForeignKey(Musica, on_delete=models.SET_NULL, null=True, blank=True, default=None)
	Fotos=models.BooleanField(blank=True, default=False)
	precio=models.BigIntegerField(default=0)
	def __str__(self):
		return self.Boda.__str__()+" -> Ceremonia: {}".format(self.id)

class DecoracionCeremonia(models.Model):
	nombre=models.CharField(max_length=50, null=True, blank=True, default=None)
	descripcion=models.TextField(max_length=1000, null=True, blank=True, default=None)
	imagen=models.ImageField(upload_to="Ceremonia/Decoracion", null=True, blank=True, default=None)
	precio=models.BigIntegerField(default=0)
	class Meta:
		verbose_name = "Decoración"
		verbose_name_plural = "Decoraciones"
	
	def __str__(self):
		return self.nombre+" -> Decoracion Ceremonia: {}".format(self.id)

class DecoracionCeremoniaCarrito(models.Model):
	Decoracion=models.ForeignKey(DecoracionCeremonia, on_delete=models.CASCADE)
	CeremoniaEvento=models.ForeignKey(CeremoniaEvento, on_delete=models.CASCADE)
	cantidad=models.IntegerField()
	subtotal = models.BigIntegerField(default=0)
	def __str__(self):
		return self.CeremoniaEvento.__str__()+" <-> "+self.Decoracion.__str__()+" -> Decoracion Ceremonia Carrito: {}".format(self.id)