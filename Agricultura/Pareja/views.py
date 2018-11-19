from django.shortcuts import render
from django.shortcuts import redirect
from django.template.loader import get_template
from django.contrib.auth import logout
from django.http import HttpResponse

from django.template import loader

from .models import *
from Domain.models import *
from Ceremonia.models import *
from Fiesta.models import *
from Ceremonia.models import *
from LunaMiel.models import *


from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .utils import getPriceFormat

@login_required(login_url='index')
def TableroResumen(request):	
	user_id = request.user
	enamorado = Enamorado.objects.get(User_id=user_id)
	boda = Boda.objects.filter(Enamorado1_id=enamorado.id)

	if len(boda) == 0:
		boda = Boda.objects.filter(Enamorado2_id=enamorado.id)    

	fiesta = FiestaEvento.objects.get(Boda_id=boda[0].id)
	ceremonia = CeremoniaEvento.objects.get(Boda_id=boda[0].id)
	luna = LunaMielEvento.objects.get(Boda_id=boda[0].id)
	precio_pareja = int(boda[0].Enamorado1.precio) + int(boda[0].Enamorado2.precio)


	if fiesta.Lugar != None:
		precio = getPriceFormat(fiesta.Lugar.precio)
		fiesta.Lugar.precioSTR = precio

	entretenimientos = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	alimentos = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	decoraciones = DecoracionCeremoniaCarrito.objects.filter(CeremoniaEvento_id=ceremonia.id)

	actividades_luna = ActividadCarrito.objects.filter(LunaMielEvento_id=luna.id)
	hoteles_luna = HotelCarrito.objects.filter(LunaMielEvento_id=luna.id)


	flag_hotel = False
	flag_acti = False
	if len(actividades_luna) > 0:
		flag_acti = True

	if len(hoteles_luna) > 0:
		flag_hotel = True

	flag_deco = False
	if len(decoraciones) > 0:
		flag_deco = True

	precio_entretenimiento = 0
	for entre in entretenimientos:
		precio_entretenimiento += entre.Entretenimiento.precio
	if len(entretenimientos) > 0:
		precio_entre = (True , getPriceFormat(precio_entretenimiento))
	else:
		precio_entre = (False , "")

	precio_alimento = 0
	for alimento in alimentos:
		precio_alimento += alimento.subtotal
	if len(alimentos) > 0:
		precio_alim = (True, getPriceFormat(precio_alimento))
	else:
		precio_alim = (False , "")

	enamorado1 = boda[0].Enamorado1
	enamorado2 = boda[0].Enamorado2

	bellezasE1 = BellezaCarrito.objects.filter(Enamorado_id=enamorado1.id)
	bellezasE2 = BellezaCarrito.objects.filter(Enamorado_id=enamorado2.id)

	prendasE1 = PrendaCarrito.objects.filter(Enamorado_id=enamorado1.id)
	prendasE2 = PrendaCarrito.objects.filter(Enamorado_id=enamorado2.id)

	AccesorioE1 = AccesorioCarrito.objects.filter(Enamorado_id=enamorado1.id)
	AccesorioE2 = AccesorioCarrito.objects.filter(Enamorado_id=enamorado2.id)


	flag_belleza1 = False
	flag_belleza2 = False

	flag_prenda1 = False
	flag_prenda2 = False

	flag_accesorio1 = False
	flag_accesorio2 = False

	if len(prendasE1) > 0:
		flag_prenda1 = True

	if len(prendasE2) > 0:
		flag_prenda2 = True

	if len(bellezasE1) > 0:
		flag_belleza1 = True

	if len(bellezasE2) > 0:
		flag_belleza2 = True

	if len(AccesorioE1) > 0:
		flag_accesorio1 = True

	if len(AccesorioE2) > 0:
		flag_accesorio2 = True

	ctx={
		'user_id': user_id,
		'fiesta':fiesta,
		'ceremonia' : ceremonia,
		'boda_id':boda[0].id,
		'fiesta_id':fiesta.id,
		'ceremonia_id':ceremonia.id,
		'precio_fiesta': getPriceFormat(fiesta.precio),
		'precio_ceremonia': getPriceFormat(ceremonia.precio),
		'precio_luna': getPriceFormat(luna.precio),
		'precio_enamorado': getPriceFormat(boda[0].Enamorado1.precio),
		'precio_enamorado2': getPriceFormat(boda[0].Enamorado2.precio),
		'enamoradoNombre': boda[0].Enamorado1,
		'enamoradoNombre2': boda[0].Enamorado2,
		'precio_pareja': getPriceFormat(precio_pareja),
		'precio_boda': getPriceFormat(boda[0].precio),
		'precio_entre': precio_entre,
		'precio_alim': precio_alim,
		'flag_deco': flag_deco,
		'flag_belleza1': flag_belleza1,
		'flag_belleza2': flag_belleza2,
		'flag_prenda1': flag_prenda1,
		'flag_prenda2': flag_prenda2,
		'flag_accesorio1': flag_accesorio1,
		'flag_accesorio2': flag_accesorio2,
		'flag_activi' : flag_acti,
		'flag_hotel': flag_hotel		
	}
	template = loader.get_template('TableroResumen.html')

	return HttpResponse(template.render(ctx, request))


def Index(request):
	ctx={}
	template = loader.get_template('Pareja/index.html')

	return HttpResponse(template.render(ctx, request))
	
def Logout(request):
	if request.user is not None:

		logout(request)
	return redirect('index')

@login_required(login_url='index')
def Enamorado1(request): 

	user_id=request.user
	enamorado = Enamorado.objects.get(User_id=user_id)

	try:
		boda=Boda.objects.get(Enamorado2=enamorado)  
		
	except :
		boda=Boda.objects.get(Enamorado1=enamorado)    

	fiesta = FiestaEvento.objects.get(Boda_id=boda.id)
	ceremonia = CeremoniaEvento.objects.get(Boda_id=boda.id)
	luna = LunaMielEvento.objects.get(Boda_id=boda.id)
	enamorado1=boda.Enamorado1
	enamorado2=boda.Enamorado2
	mensaje_error = (False , "")

	mensaje_succes = (False , "")

	mensaje_delete = (False , "") 
	lista_prendas=[]
	lista_bellezas=[]
	lista_accesorios=[]    
	if request.method == 'GET':#Este metodo deberia quitarse

		


		
		#LISTADO DE PRODUCTOS
		Bellezas = Belleza.objects.all()

		Prendas = Prenda.objects.all()
		PrendasMas=Prenda.objects.filter(tipo='masculino')
		PrendasFem=Prenda.objects.filter(tipo='femenino')
		PrendasMix=Prenda.objects.filter(tipo='mixto')


		Accesorios = Accesorio.objects.all()
		#LISTADO DE OBJETOS ALAMCENADOS EN EL CARRITO DEL PRIMER ENAMORADO
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado1.id)

		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado1.id)

		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado1.id)   

		#LISTADO DE OBJETOS ALAMCENADOS EN EL CARRITO DEL segundo ENAMORADO
		belleza2 = BellezaCarrito.objects.filter(Enamorado_id=enamorado2.id)

		prenda2 = PrendaCarrito.objects.filter(Enamorado_id=enamorado2.id)

		accesorio2=AccesorioCarrito.objects.filter(Enamorado_id=enamorado2.id) 

		template = loader.get_template('Pareja/pareja.html')
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado1.id) 

		lista_prendas.clear()
		lista_accesorios.clear()
		lista_bellezas.clear()  
		#Cagar listas con lo adquirido actualmente            
		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id)                           
		#enamorado1.precio=0
		#enamorado1.save()
		context = {

			'enamorado' : enamorado1,
			#'enamorado2' : enamorado2,

			'belleza' : belleza,
			#'belleza2' : belleza2,

			'Bellezas' : Bellezas,

			'prenda' : prenda,
			#'prenda2' : prenda2,
			'Prendas' : Prendas,

			'accesorio' : accesorio,
			#'accesorio2' : accesorio2,

			'Accesorios' : Accesorios,
			'PrendasMas':PrendasMas,
			'PrendasFem':PrendasFem,
			'PrendasMix':PrendasMix,
			'precio' : getPriceFormat(enamorado1.precio),
			'lista_prendas': lista_prendas,
			'lista_bellezas': lista_bellezas,
			'lista_accesorios':lista_accesorios,
			'user_id': user_id,
			'boda_id':boda.id,
			'fiesta_id':fiesta.id,
			'ceremonia_id':ceremonia.id,
			'enamoradoNombre': enamorado1,
			'enamoradoNombre2': enamorado2
		}

		return HttpResponse(template.render(context, request))    
	


	if request.method == 'POST':

	
		#LISTADO DE PRODUCTOS
		Bellezas = Belleza.objects.all()
		Prendas = Prenda.objects.all()
		PrendasMas=Prenda.objects.filter(tipo='masculino')
		PrendasFem=Prenda.objects.filter(tipo='femenino')
		PrendasMix=Prenda.objects.filter(tipo='mixto')

		Accesorios = Accesorio.objects.all()

		#LISTADO DE OBJETOS ALAMCENADOS EN EL CARRITO DEL PRIMER ENAMORADO
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado1.id)            
		
		#Cagar listas con lo adquirido actualmente            
		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id)                                
		value_btn = request.POST.get('btn_value')
		#AGREGAR PRENDA
		if value_btn == "add_prenda":            
			prenda_id = request.POST.get('id_prenda')
			precio=request.POST.get('price')
			if int(prenda_id) not in lista_prendas:
				enamorado1.precio=enamorado1.precio + int(precio)             
				enamorado1.save()   
				boda.precio = int(boda.precio) + int(precio)
				boda.save()   
				prend=Prenda.objects.filter(id__exact=prenda_id)
				prenaux=PrendaCarrito.objects.create(Enamorado=enamorado1,Prenda=prend[0])
				prenaux.save()
				lista_prendas.clear()
				mensaje_succes = (True , "Tu prenda fue agregada correctamente")
				if prenda.count()>0:
					for a in prenda:
						lista_prendas.append(a.Prenda.id)                      
			else:
				mensaje_error=  (True , "Esta prenda ya fue agregada")


		#AGREGAR BELLEZA
		if value_btn == "add_belleza":
			belleza_id = request.POST.get('id_belleza')
			precio=request.POST.get('price')
			if int(belleza_id) not in lista_bellezas:
				enamorado1.precio=enamorado1.precio + int(precio)               
				enamorado1.save()
				boda.precio = int(boda.precio) + int(precio)
				boda.save()
				bell=Belleza.objects.filter(id__exact=belleza_id)
				bellaux=BellezaCarrito.objects.create(Enamorado=enamorado1,Belleza=bell[0])
				bellaux.save()   
				lista_bellezas.clear()
				mensaje_succes = (True , "Tu belleza fue agregada correctamente")
				if belleza.count()>0:
					for a in belleza:
						lista_bellezas.append(a.Belleza.id)                
			else:
				mensaje_error=  (True , "Esta belleza ya fue agregada")


		if value_btn == "add_accesorio":            
			accesorio_id = request.POST.get('id_accesorio')
			precio=request.POST.get('price')
			if int(accesorio_id) not in lista_accesorios:    
				enamorado1.precio=enamorado1.precio + int(precio)               
				enamorado1.save()
				boda.precio = int(boda.precio) + int(precio)
				boda.save()   
				acce=Accesorio.objects.filter(id__exact=accesorio_id)
				acceaux=AccesorioCarrito.objects.create(Enamorado=enamorado1,Accesorio=acce[0])
				acceaux.save()    
				lista_accesorios.clear()        
				mensaje_succes = (True , "Tu accesorio fue agregada correctamente") 
				if accesorio.count()>0:
					for a in accesorio:
						lista_accesorios.append(a.Accesorio.id)                
			else:
				mensaje_error=  (True , "Este accesorio ya fue agregado") 
					


		if value_btn == "delete_accesorio":
			accesorio_id = request.POST.get('accesorio_id')
			precio=request.POST.get('price')
			if int(accesorio_id)  in lista_accesorios:
				enamorado1.precio=enamorado1.precio - int(precio)
				enamorado1.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_accesorio_id = request.POST.get('carrito_accesorio_id')
				accesoriocarrito = AccesorioCarrito.objects.filter(id__exact=carrito_accesorio_id)
				accesoriocarrito.delete()
				mensaje_delete = (True , "Accesorio eliminado correctamente")
				lista_accesorios.clear()
				if accesorio.count()>0:
					for a in accesorio:
						lista_accesorios.append(a.Accesorio.id)                
			else:
				mensaje_error=  (True , "Este accesorio ya ha sido eliminado") 

			
		if value_btn == "delete_belleza":
			belleza_id = request.POST.get('belleza_id')
			if int(belleza_id)  in lista_bellezas:
				precio=request.POST.get('price')              
				enamorado1.precio=enamorado1.precio - int(precio)
				enamorado1.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_belleza_id = request.POST.get('carrito_belleza_id')
				bellezacarrito = BellezaCarrito.objects.filter(id__exact=carrito_belleza_id)
				bellezacarrito.delete()
				mensaje_delete = (True , "Belleza eliminada correctamente")
				lista_bellezas.clear()
				if belleza.count()>0:
					for a in belleza:
						lista_bellezas.append(a.Belleza.id)                  
			else:     
				mensaje_error=  (True , "Esta belleza ya ha sido eliminada") 

		if value_btn == "delete_prenda":
			prenda_id = request.POST.get('prenda_id')
			if int(prenda_id)  in lista_prendas:
				precio=request.POST.get('price')               
				enamorado1.precio=enamorado1.precio - int(precio)
				enamorado1.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_prenda_id = request.POST.get('carrito_prenda_id')
				prendacarrito = PrendaCarrito.objects.filter(id__exact=carrito_prenda_id)
				prendacarrito.delete()
				mensaje_delete = (True , "Prenda eliminada correctamente")
				lista_prendas.clear()
				if prenda.count()>0:
					for a in prenda:
						lista_prendas.append(a.Prenda.id)  
			else:     
				mensaje_error=  (True , "Esta prenda ya ha sido eliminada")                        

		template = get_template('Pareja/pareja.html')
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado1.id)
		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado1.id)
		#Cagar listas con lo adquirido actualmente  
		lista_prendas.clear()
		lista_accesorios.clear()
		lista_bellezas.clear()  

		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id) 
		context = {



			'enamorado' : enamorado1,
			#'enamorado2' : enamorado2,

			'belleza' : belleza,
			#'belleza2' : belleza2,

			'Bellezas' : Bellezas,

			'prenda' : prenda,
			#'prenda2' : prenda2,
			'Prendas' : Prendas,

			'accesorio' : accesorio,
			#'accesorio2' : accesorio2,

			'Accesorios' : Accesorios,
			'PrendasMas':PrendasMas,
			'PrendasFem':PrendasFem,
			'PrendasMix':PrendasMix,
			'precio' : getPriceFormat(enamorado1.precio),
			'mensaje_succes' : mensaje_succes,
			'lista_prendas': lista_prendas,
			'lista_bellezas': lista_bellezas,
			'lista_accesorios':lista_accesorios,
			'mensaje_delete' : mensaje_delete,
			'mensaje_error' : mensaje_error,            
			'user_id': user_id,
			'boda_id':boda.id,
			'fiesta_id':fiesta.id,
			'ceremonia_id':ceremonia.id,
			'enamoradoNombre': enamorado1,
			'enamoradoNombre2': enamorado2
		}          
		return HttpResponse(template.render(context, request))       
	
#Se debe establecer por medio de url por parametros una vista unificada
@login_required(login_url='index')
def Enamorado2(request):  

	mensaje_error = (False , "")

	mensaje_succes = (False , "")

	mensaje_delete = (False , "") 
	lista_prendas=[]
	lista_bellezas=[]
	lista_accesorios=[]   

	user_id=request.user
	enamorado = Enamorado.objects.get(User_id=user_id)

	try:
		boda=Boda.objects.get(Enamorado2=enamorado)  
		
	except :
		boda=Boda.objects.get(Enamorado1=enamorado)    

	fiesta = FiestaEvento.objects.get(Boda_id=boda.id)
	ceremonia = CeremoniaEvento.objects.get(Boda_id=boda.id)
	luna = LunaMielEvento.objects.get(Boda_id=boda.id)

	if request.method == 'GET':#Este metodo deberia qutiarse

		


		enamorado1=boda.Enamorado1
		enamorado2=boda.Enamorado2
		#LISTADO DE PRODUCTOS
		Bellezas = Belleza.objects.all()

		Prendas = Prenda.objects.all()
		PrendasMas=Prenda.objects.filter(tipo='masculino')
		PrendasFem=Prenda.objects.filter(tipo='femenino')
		PrendasMix=Prenda.objects.filter(tipo='mixto')


		Accesorios = Accesorio.objects.all()
  

		#LISTADO DE OBJETOS ALAMCENADOS EN EL CARRITO DEL segundo ENAMORADO
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado2.id)

		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado2.id)

		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado2.id) 

		template = loader.get_template('Pareja/pareja.html')


		lista_prendas.clear()
		lista_accesorios.clear()
		lista_bellezas.clear()  
		#Cagar listas con lo adquirido actualmente            
		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id)                           
		#enamorado1.precio=0
		#enamorado1.save()
		context = {

			'enamorado' : enamorado2,
			#'enamorado2' : enamorado2,

			'belleza' : belleza,
			#'belleza2' : belleza2,

			'Bellezas' : Bellezas,

			'prenda' : prenda,
			#'prenda2' : prenda2,
			'Prendas' : Prendas,

			'accesorio' : accesorio,
			#'accesorio2' : accesorio2,

			'Accesorios' : Accesorios,
			'PrendasMas':PrendasMas,
			'PrendasFem':PrendasFem,
			'PrendasMix':PrendasMix,
			'precio' : getPriceFormat(enamorado2.precio),
			'lista_prendas': lista_prendas,
			'lista_bellezas': lista_bellezas,
			'lista_accesorios':lista_accesorios,
			'user_id': user_id,
			'boda_id':boda.id,
			'fiesta_id':fiesta.id,
			'ceremonia_id':ceremonia.id,
			'enamoradoNombre': enamorado1,
			'enamoradoNombre2': enamorado2
		}

		return HttpResponse(template.render(context, request))    
	


	if request.method == 'POST':
  

		enamorado1=boda.Enamorado1
		enamorado2=boda.Enamorado2
		#LISTADO DE PRODUCTOS
		Bellezas = Belleza.objects.all()
		Prendas = Prenda.objects.all()
		PrendasMas=Prenda.objects.filter(tipo='masculino')
		PrendasFem=Prenda.objects.filter(tipo='femenino')
		PrendasMix=Prenda.objects.filter(tipo='mixto')

		Accesorios = Accesorio.objects.all()

		#LISTADO DE OBJETOS ALAMCENADOS EN EL CARRITO DEL SEGUNDO ENAMORADO
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado2.id)
		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado2.id)
		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado2.id)            
		
		#Cagar listas con lo adquirido actualmente            
		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id)                                
		value_btn = request.POST.get('btn_value')
		#AGREGAR PRENDA
		if value_btn == "add_prenda":            
			prenda_id = request.POST.get('id_prenda')
			precio=request.POST.get('price')
			if int(prenda_id) not in lista_prendas:
				enamorado2.precio=enamorado2.precio + int(precio)             
				enamorado2.save()
				boda.precio = int(boda.precio) + int(precio)
				boda.save()
				prend=Prenda.objects.filter(id__exact=prenda_id)
				prenaux=PrendaCarrito.objects.create(Enamorado=enamorado2,Prenda=prend[0])
				prenaux.save()
				lista_prendas.clear()
				mensaje_succes = (True , "Tu prenda fue agregada correctamente")
				if prenda.count()>0:
					for a in prenda:
						lista_prendas.append(a.Prenda.id)                      
			else:
				mensaje_error=  (True , "Esta prenda ya fue agregada")


		#AGREGAR BELLEZA
		if value_btn == "add_belleza":
			belleza_id = request.POST.get('id_belleza')
			precio=request.POST.get('price')
			if int(belleza_id) not in lista_bellezas:
				enamorado2.precio=enamorado2.precio + int(precio)               
				enamorado2.save()
				boda.precio = int(boda.precio) + int(precio)
				boda.save()
				bell=Belleza.objects.filter(id__exact=belleza_id)
				bellaux=BellezaCarrito.objects.create(Enamorado=enamorado2,Belleza=bell[0])
				bellaux.save()   
				lista_bellezas.clear()
				mensaje_succes = (True , "Tu belleza fue agregada correctamente")
				if belleza.count()>0:
					for a in belleza:
						lista_bellezas.append(a.Belleza.id)                
			else:
				mensaje_error=  (True , "Esta belleza ya fue agregada")


		if value_btn == "add_accesorio":            
			accesorio_id = request.POST.get('id_accesorio')
			precio=request.POST.get('price')
			if int(accesorio_id) not in lista_accesorios:    
				enamorado2.precio=enamorado2.precio + int(precio)               
				enamorado2.save()
				boda.precio = int(boda.precio) + int(precio)
				boda.save()
				acce=Accesorio.objects.filter(id__exact=accesorio_id)
				acceaux=AccesorioCarrito.objects.create(Enamorado=enamorado2,Accesorio=acce[0])
				acceaux.save()    
				lista_accesorios.clear()        
				mensaje_succes = (True , "Tu accesorio fue agregada correctamente") 
				if accesorio.count()>0:
					for a in accesorio:
						lista_accesorios.append(a.Accesorio.id)                
			else:
				mensaje_error=  (True , "Este accesorio ya fue agregado") 
					


		if value_btn == "delete_accesorio":
			accesorio_id = request.POST.get('accesorio_id')
			precio=request.POST.get('price')
			if int(accesorio_id)  in lista_accesorios:
				enamorado2.precio=enamorado2.precio - int(precio)
				enamorado2.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_accesorio_id = request.POST.get('carrito_accesorio_id')
				accesoriocarrito = AccesorioCarrito.objects.filter(id__exact=carrito_accesorio_id)
				accesoriocarrito.delete()
				mensaje_delete = (True , "Accesorio eliminado correctamente")
				lista_accesorios.clear()
				if accesorio.count()>0:
					for a in accesorio:
						lista_accesorios.append(a.Accesorio.id)                
			else:
				mensaje_error=  (True , "Este accesorio ya ha sido eliminado") 

			
		if value_btn == "delete_belleza":
			belleza_id = request.POST.get('belleza_id')
			if int(belleza_id)  in lista_bellezas:
				precio=request.POST.get('price')              
				enamorado2.precio=enamorado2.precio - int(precio)
				enamorado2.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_belleza_id = request.POST.get('carrito_belleza_id')
				bellezacarrito = BellezaCarrito.objects.filter(id__exact=carrito_belleza_id)
				bellezacarrito.delete()
				mensaje_delete = (True , "Belleza eliminada correctamente")
				lista_bellezas.clear()
				if belleza.count()>0:
					for a in belleza:
						lista_bellezas.append(a.Belleza.id)                  
			else:     
				mensaje_error=  (True , "Esta belleza ya ha sido eliminada") 

		if value_btn == "delete_prenda":
			prenda_id = request.POST.get('prenda_id')
			if int(prenda_id)  in lista_prendas:
				precio=request.POST.get('price')               
				enamorado2.precio=enamorado2.precio - int(precio)
				enamorado2.save()
				boda.precio = int(boda.precio) - int(precio)
				boda.save()
				carrito_prenda_id = request.POST.get('carrito_prenda_id')
				prendacarrito = PrendaCarrito.objects.filter(id__exact=carrito_prenda_id)
				prendacarrito.delete()
				mensaje_delete = (True , "Prenda eliminada correctamente")
				lista_prendas.clear()
				if prenda.count()>0:
					for a in prenda:
						lista_prendas.append(a.Prenda.id)  
			else:     
				mensaje_error=  (True , "Esta prenda ya ha sido eliminada")                        

		template = get_template('Pareja/pareja.html')
		belleza = BellezaCarrito.objects.filter(Enamorado_id=enamorado2.id)
		prenda = PrendaCarrito.objects.filter(Enamorado_id=enamorado2.id)
		accesorio=AccesorioCarrito.objects.filter(Enamorado_id=enamorado2.id)
		lista_prendas.clear()
		lista_accesorios.clear()
		lista_bellezas.clear()  

		if prenda.count()>0:
			for a in prenda:
			   lista_prendas.append(a.Prenda.id)        
		if belleza.count()>0:
			for a in belleza:
				lista_bellezas.append(a.Belleza.id)
		if accesorio.count()>0:
			for a in accesorio:
				lista_accesorios.append(a.Accesorio.id)
		context = {



			'enamorado' : enamorado2,
			#'enamorado2' : enamorado2,

			'belleza' : belleza,
			#'belleza2' : belleza2,

			'Bellezas' : Bellezas,

			'prenda' : prenda,
			#'prenda2' : prenda2,
			'Prendas' : Prendas,

			'accesorio' : accesorio,
			#'accesorio2' : accesorio2,

			'Accesorios' : Accesorios,
			'PrendasMas':PrendasMas,
			'PrendasFem':PrendasFem,
			'PrendasMix':PrendasMix,
			'precio' : getPriceFormat(enamorado2.precio),
			'mensaje_succes' : mensaje_succes,
			'lista_prendas': lista_prendas,
			'lista_bellezas': lista_bellezas,
			'lista_accesorios':lista_accesorios,
			'mensaje_delete' : mensaje_delete,
			'mensaje_error' : mensaje_error,            
			'user_id': user_id,
			'boda_id':boda.id,
			'fiesta_id':fiesta.id,
			'ceremonia_id':ceremonia.id,
			'enamoradoNombre': enamorado1,
			'enamoradoNombre2': enamorado2
		}          
		return HttpResponse(template.render(context, request))       
		
	   
def Login(request):

	error = (False, "")
	user=None 

	if request.method == "POST":

		username = request.POST.get('username')

		password = request.POST.get('password')



		usuario = User.objects.filter(username=username)

		if len(usuario) != 0:

			user = authenticate(username=username, password=password)

			if user is not None:

				login(request, user)
				ctx = {

						'error': error, 'user': user,

				}
				return redirect('tableroResumen')

			else:

				error = (True, "Password no valida")

		else:

			error = (True, "No existe el usuario " + username)



	template = loader.get_template('Pareja/index.html')

	ctx = {

		'error': error, 

	}

	return HttpResponse(template.render(ctx, request))
# Create your views here.



def Registro(request):

		
		error = (False, "")
		mensaje = (False, "")
		template = loader.get_template('Pareja/registro.html') # get template

		if request.method == "GET":
		   
			

			ctx = {

			'mensaje': mensaje,
			'error': error,

			}                                    # Contexto o variables

			return HttpResponse(template.render(ctx, request))

		if request.method == "POST":
			#DATOS HOMMBRE
			nombre_persona1 = request.POST.get("nombreMEN")
			nombre_persona1=nombre_persona1.title()

			apellido_persona1 = request.POST.get("apellidoMEN")
			apellido_persona1= apellido_persona1.title()

			documento_persona1 = request.POST.get("identificacionMEN")

			telefono1 = request.POST.get("telefonoMEN")

			email1 = request.POST.get("emailMEN")

			#DATOS MUJER
			nombre_persona2 = request.POST.get("nombreWOMAN")
			nombre_persona2=nombre_persona2.title()

			apellido_persona2 = request.POST.get("apellidoWOMAN")
			apellido_persona2=apellido_persona2.title()

			documento_persona2 = request.POST.get("identificacionWOMAN")

			telefono2 = request.POST.get("telefonoWOMAN")

			email2 = request.POST.get("emailWOMAN")

			contrasena = request.POST.get("password")
			contrasenaAut = request.POST.get("passwordAut")
			
			users1=User.objects.filter(username=documento_persona1)
			users2=User.objects.filter(username=documento_persona2)
			if users1.count()>0 :
				error=(True,"Identificacion 1 ya existe ")
			else:
				if users2.count()>0 :
					error=(True,"Identificacion 2 ya existe ")	
				else:
					if contrasena==contrasenaAut:
						if telefono2.isdigit() and telefono1.isdigit():
							if documento_persona2.isdigit() and documento_persona1.isdigit():


								user1=User.objects.create(first_name=nombre_persona1,last_name=apellido_persona1, email=email1, username=documento_persona1)
									
								
								user1.set_password(contrasena)
								user1.save()            
								user2=User.objects.create(first_name=nombre_persona2, last_name=apellido_persona2, email=email2, username=documento_persona2)
								user2.set_password(contrasena)
								user2.save()

								#creacion enamorados
								enamorado1=Enamorado.objects.create(User=user1, cedula=documento_persona1, telefono=telefono1)
								enamorado1.save()
								enamorado2=Enamorado.objects.create(User=user2, cedula=documento_persona2, telefono=telefono2)
								enamorado2.save() 
								
								#creacion de Boda
								Boda1=Boda.objects.create(Enamorado1=enamorado1,Enamorado2=enamorado2)
								Boda1.save()
								#CREACION CEREMONIA
								CeremoniaEvento1=CeremoniaEvento.objects.create(Boda=Boda1)
								#CREACION FIESTA
								FiestaEvento1=FiestaEvento.objects.create(Boda=Boda1)
								#CREACION LUNA DE MIEL
								LunaMielEvento1=LunaMielEvento.objects.create(Boda=Boda1)
								
								#REINICIO DE DATOS
								nombre_persona1 =""


								apellido_persona1 =""
								apellido_persona1 =""

								documento_persona1 =""

								telefono1 = ""

								email1  =""

								#DATOS MUJER
								nombre_persona2  =""
								nombre_persona2=""

								apellido_persona2 =""
								apellido_persona2=""

								documento_persona2 =""

								telefono2 =""

								email2 =""
															
								mensaje = (True, "La persona fue ingresada en el sistema")
							else:
								error=(True,"La identificacion debe ser numerica")	
						else:
							error=(True,"El telefono debe ser numerico")	
					else:
						error=(True,"Contraseña no coincide")

			ctx = {

			'mensaje': mensaje,
			'error': error,
			'nombre_persona1':nombre_persona1,
			'apellido_persona1':apellido_persona1,
			'documento_persona1':documento_persona1,
			'telefono1': telefono1,
			'email1':email1,
			'nombre_persona2':nombre_persona2,
			'apellido_persona2':apellido_persona2,
			'documento_persona2':documento_persona2,
			'telefono2': telefono2,
			'email2':email2,

			}                  
			return HttpResponse(template.render(ctx, request))
