from django.http import HttpResponse
from django.template.loader import get_template
from Domain.models import Boda
from Domain.models import Lugar
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from Domain.models import *
from .models import *
from Fiesta.models import FiestaEvento

# Create your views here.

@login_required(login_url='index')
def ceremoniaDashboardView(request, user_id , boda_id , ceremonia_id):
	
	if str(request.user) != str(user_id):
		logout(request)
		return redirect('index')

	user_id = request.user
	enamorado = Enamorado.objects.get(User_id=user_id)
	indices_decoraciones = []

	try:
		boda2 = Boda.objects.get(Enamorado1_id=enamorado.id)
	except:
		boda2 = Boda.objects.get(Enamorado2_id=enamorado.id)
	

	if str(boda2.id) != str(boda_id):
		return redirect('tableroResumen')

	boda = Boda.objects.filter(id__exact=boda_id)
	ceremonia = CeremoniaEvento.objects.get(Boda_id=boda_id)

	fiesta = FiestaEvento.objects.get(Boda_id=boda_id)


	if str(ceremonia_id) != str(ceremonia.id):
		return redirect('tableroResumen')

	count_deco = DecoracionCeremoniaCarrito.objects.all()


	if len(count_deco) > 0:
		flag_decoracion = True
	else:
		flag_decoracion = False

	if ceremonia.Ministro != None:
		flag_ministro = True
	else:
		flag_ministro = False

	if ceremonia.Lugar != None:
		flag_lugar = True
	else:
		flag_lugar = False

	if ceremonia.Musica != None:
		flag_musica = True
	else:
		flag_musica = False

	if ceremonia.Fotos != False:
		flag_fotos = True
	else:
		flag_fotos = False



	if request.method == 'GET':

		ministros = Ministro.objects.all()
		lugares = Lugar.objects.filter(tipo='ceremonia')
		musicas = Musica.objects.all()
		boda = Boda.objects.get(id=boda_id)
		decoraciones = DecoracionCeremonia.objects.all()
		decoraciones_car = DecoracionCeremoniaCarrito.objects.filter(CeremoniaEvento_id=ceremonia_id)

		indices_decoraciones.clear()

		if decoraciones_car.count() > 0:
			indices_decoraciones.clear()
			for deco in decoraciones_car:
				indices_decoraciones.append(deco.Decoracion.id)



		template = get_template('Ceremonia/ceremonia.html')
		ctx={

			'ministros' : ministros,
			'flag_ministro': flag_ministro,
			'flag_fotos': flag_fotos,
			'flag_lugar': flag_lugar,
			'flag_musica': flag_musica,
			'ceremonia' : ceremonia,
			'lugares' : lugares,
			'musicas' : musicas,
			'decoraciones':decoraciones,
			'decoraciones_car':decoraciones_car,
			'flag_decoracion':flag_decoracion,
			'indices_decoraciones': indices_decoraciones,
			'user_id': user_id,
			'boda_id': boda_id,
			'ceremonia_id' : ceremonia.id,
			'fiesta_id': fiesta.id,
			'enamoradoNombre': boda.Enamorado1,
			'enamoradoNombre2': boda.Enamorado2

		}
		return HttpResponse(template.render(ctx,request))

	if request.method == 'POST':
		ceremonia = CeremoniaEvento.objects.get(Boda_id=boda_id)
		boda = Boda.objects.get(id=boda_id)
		btn_value = request.POST.get('btn_value')
		decoraciones_car = DecoracionCeremoniaCarrito.objects.filter(CeremoniaEvento_id=ceremonia_id)
		indices_decoraciones.clear()

		if decoraciones_car.count() > 0:
			indices_decoraciones.clear()
			for deco in decoraciones_car:
				indices_decoraciones.append(deco.Decoracion.id)


		if btn_value == 'add_ministro':
			if not 	flag_ministro:
				price = request.POST.get('price')
				id_ministro = request.POST.get('id_ministro')
				ceremonia.Ministro_id = id_ministro
				ceremonia.precio = ceremonia.precio + int(price)
				flag_ministro = True
				boda.precio = boda.precio + int(price)
				boda.save()
				ceremonia.save()
			else:
				pass

		if btn_value == 'add_lugar':
			if not flag_lugar:
				price = request.POST.get('price')
				id_ministro = request.POST.get('id_lugar')
				ceremonia.Lugar_id = id_ministro
				ceremonia.precio = ceremonia.precio + int(price)
				flag_lugar = True
				boda.precio = boda.precio + int(price)
				boda.save()
				ceremonia.save()
			else:
				pass

		if btn_value == 'add_musica':
			if not flag_musica:
				price = request.POST.get('price')
				id_musica = request.POST.get('id_musica')
				ceremonia.Musica_id = id_musica
				ceremonia.precio = ceremonia.precio + int(price)
				flag_musica = True
				boda.precio = boda.precio + int(price)
				boda.save()
				ceremonia.save()
			else:
				pass

		if btn_value == 'add_fotos':
			if not flag_fotos:
				ceremonia.Fotos = True
				flag_fotos = True
				ceremonia.save()
			else:
				pass

		if btn_value == 'delete_ministro':
			if flag_ministro:
				price = request.POST.get('price')
				ceremonia.Ministro_id = None
				ceremonia.precio = ceremonia.precio - int(price)
				flag_ministro = False
				boda.precio = boda.precio - int(price)
				boda.save()
				ceremonia.save()
			else:
				pass

		if btn_value == 'delete_lugar':
			if flag_lugar:
				price = request.POST.get('price')
				ceremonia.Lugar_id = None
				ceremonia.precio = ceremonia.precio - int(price)
				flag_lugar = False
				boda.precio = boda.precio - int(price)
				boda.save()
				ceremonia.save()
			else:
				pass

		if btn_value == 'delete_musica':
			if flag_musica:
				price = request.POST.get('price')
				ceremonia.Musica_id = None
				ceremonia.precio = ceremonia.precio - int(price)
				flag_musica = False
				boda.precio = boda.precio - int(price)
				boda.save()
				ceremonia.save()
			else:
				pass


		if btn_value == "add_decoracion":
			cantidad = request.POST.get('cantidad')
			flag_decoracion = True
			id_decoracion = request.POST.get('id_decoracion')
			price = request.POST.get('price')
			decoracion = DecoracionCeremonia.objects.filter(id__exact=id_decoracion)

			if int(id_decoracion) not in indices_decoraciones:
				decoracion_carrito = DecoracionCeremoniaCarrito(Decoracion=decoracion[0] , CeremoniaEvento = ceremonia , cantidad = cantidad , subtotal=(int(price) * int (cantidad)))
				ceremonia.precio = ceremonia.precio + (int(price) * int (cantidad))
				boda.precio = boda.precio + (int(price) * int(cantidad))
				boda.save()
				ceremonia.save()
				decoracion_carrito.save()
				indices_decoraciones.clear()

				if decoraciones_car.count() > 0:
					for deco in decoraciones_car:
						indices_decoraciones.append(deco.Decoracion.id)

			else:
				pass

		if btn_value == "delete_decoracion":
			decoracion_id = request.POST.get('id_decoracion')

			if int(decoracion_id) in indices_decoraciones:
				decoracion_carrito_id = request.POST.get('id_decoracion_carrito')
				decoracioncarrito = DecoracionCeremoniaCarrito.objects.filter(id__exact=decoracion_carrito_id)
				cantidad = decoracioncarrito[0].cantidad
				decoracioncarrito.delete()
				price = request.POST.get('price')
				ceremonia.precio = ceremonia.precio - (int(cantidad)  * int(price))
				boda.precio = boda.precio - (int(price) * int(cantidad))
				boda.save()
				ceremonia.save()
				indices_decoraciones.clear()

				if decoraciones_car.count() > 0:
					for deco in decoraciones_car:
						indices_decoraciones.append(deco.Decoracion.id)
			else:
				pass

		if btn_value == 'delete_fotos':
			ceremonia.Fotos = False
			flag_fotos = False
			ceremonia.save()


		ministros = Ministro.objects.all()
		musicas = Musica.objects.all()
		lugares = Lugar.objects.filter(tipo='ceremonia')
		decoraciones = DecoracionCeremonia.objects.all()
		decoraciones_car = DecoracionCeremoniaCarrito.objects.filter(CeremoniaEvento_id=ceremonia_id)

		indices_decoraciones.clear()

		if decoraciones_car.count() > 0:
			for deco in decoraciones_car:
				indices_decoraciones.append(deco.Decoracion.id)

		template = get_template('Ceremonia/ceremonia.html')
		ctx={

			'ministros' : ministros,
			'flag_ministro': flag_ministro,
			'flag_fotos': flag_fotos,
			'flag_lugar': flag_lugar,
			'flag_musica': flag_musica,
			'flag_decoracion':flag_decoracion,
			'ceremonia' : ceremonia,
			'lugares' : lugares,
			'musicas' : musicas,
			'decoraciones':decoraciones,
			'decoraciones_car':decoraciones_car,
			'indices_decoraciones': indices_decoraciones,
			'user_id': user_id,
			'boda_id': boda_id,
			'ceremonia_id' : ceremonia.id,
			'fiesta_id': fiesta.id,
			'enamoradoNombre': boda.Enamorado1,
			'enamoradoNombre2': boda.Enamorado2


		}
		return HttpResponse(template.render(ctx,request))
	
