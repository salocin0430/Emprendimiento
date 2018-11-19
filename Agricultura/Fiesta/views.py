from django.http import HttpResponse
from django.template.loader import get_template
from Domain.models import Boda
from Domain.models import Lugar
from .models import FiestaEvento, AlimentoCarrito, Alimento, EntretenimientoCarrito, Entretenimiento
from Ceremonia.models import CeremoniaEvento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from Domain.models import *

from .utils import getPriceFormat

@login_required(login_url='index')
def fiestaDashboardView(request, user_id , boda_id , fiesta_id):

	if str(request.user) != str(user_id):
		logout(request)
		return redirect('index')

	user_id = request.user
	enamorado = Enamorado.objects.get(User_id=user_id)

	try:
		boda2 = Boda.objects.get(Enamorado1_id=enamorado.id)
	except:
		boda2 = Boda.objects.get(Enamorado2_id=enamorado.id)
	

	if str(boda2.id) != str(boda_id):
		return redirect('tableroResumen')

	boda = Boda.objects.filter(id__exact=boda_id)
	fiesta = FiestaEvento.objects.get(Boda_id=boda_id)
	ceremonia = CeremoniaEvento.objects.get(Boda_id=boda_id)


	alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	indices_alimentos = []
	indices_entretenimientos = []
	mensaje_error = (False , "")
	mensaje_succes = (False , "")
	mensaje_delete = (False , "")
	subtotal = ""

	if str(fiesta_id) != str(fiesta.id):
		return redirect('tableroResumen')

	Lugares = Lugar.objects.filter(tipo='fiesta')

	for indexLugar in range(0, len(Lugares)):
		precio = getPriceFormat(Lugares[indexLugar].precio)
		Lugares[indexLugar].precioSTR = precio

	if fiesta.Lugar:
		fiesta.Lugar.precioSTR = getPriceFormat(fiesta.Lugar.precio)


	alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	indices_alimentos = []
	indices_entretenimientos = []

	count_entre = EntretenimientoCarrito.objects.all()
	count_comida = AlimentoCarrito.objects.all()

	flag_entre = len(count_entre) > 0
	flag_comida = len(count_comida) > 0
	flag_place = fiesta.Lugar != None
	flag_foto = fiesta.Fotos

	Fiesta = None
	if request.method == 'GET':
		Alimentos = Alimento.objects.all()
		Entretenimientos = Entretenimiento.objects.all()
		alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
		entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)

		for indexAlimento in range(0, len(Alimentos)):
			precio = getPriceFormat(Alimentos[indexAlimento].precio)
			Alimentos[indexAlimento].precioSTR = precio

		for food in alimento:
			precio = getPriceFormat(food.Alimento.precio)
			precioSub = getPriceFormat(food.subtotal)
			food.subtotal = precioSub
			food.Alimento.precioSTR = precio

		for indexEntre in range(0, len(Entretenimientos)):
			precio = getPriceFormat(Entretenimientos[indexEntre].precio)
			Entretenimientos[indexEntre].precioSTR = precio

		for entre in entretenimiento:
			precio = getPriceFormat(entre.Entretenimiento.precio)
			entre.Entretenimiento.precioSTR = precio


		indices_alimentos.clear()
		indices_entretenimientos.clear()

		if alimento.count() > 0:
			for a in alimento:
				indices_alimentos.append(a.Alimento.id)

		if entretenimiento.count() > 0:
			for e in entretenimiento:
				indices_entretenimientos.append(e.Entretenimiento.id)

		if boda_id != 0:
			boda = Boda.objects.filter(id__exact=boda_id)

			template = get_template('Fiesta/fiesta.html')

		size_alimentos = len(indices_alimentos)
		size_entre = len(indices_entretenimientos)
		limite = 0

		flag_comida = size_alimentos > limite
		flag_entre = size_entre > limite

		context = {
			'Lugares' : Lugares,
			'flag_place' : flag_place,
			'flag_foto' : flag_foto,
			'flag_entre' : flag_entre,
			'flag_comida' : flag_comida,
			'fiesta' : fiesta,
			'alimento' : alimento,
			'Alimentos' : Alimentos,
			'indices_alimentos' : indices_alimentos,
			'entretenimiento' : entretenimiento,
			'Entretenimientos' : Entretenimientos,
			'indices_entretenimientos' : indices_entretenimientos,
			'precio' : getPriceFormat(fiesta.precio),
			'user_id': user_id,
			'boda_id': boda_id,
			'fiesta_id':fiesta_id,
			'ceremonia_id':ceremonia.id,
			'enamoradoNombre': boda[0].Enamorado1,
			'enamoradoNombre2': boda[0].Enamorado2
		}
		return HttpResponse(template.render(context, request))

	if request.method == 'POST':
		fiesta = FiestaEvento.objects.get(Boda_id=boda_id)
		boda = Boda.objects.get(id=boda_id)
		value_btn = request.POST.get('btn_value')
		Alimentos = Alimento.objects.all()
		alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
		Entretenimientos = Entretenimiento.objects.all()
		entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)


		if alimento.count() > 0:
			indices_alimentos.clear()
			for a in alimento:
				indices_alimentos.append(a.Alimento.id)

		if entretenimiento.count() > 0:
			for e in entretenimiento:
				indices_entretenimientos.append(e.Entretenimiento.id)

		if value_btn == "add_place":
			if flag_place == False:
				id_place = request.POST.get('id_place')
				price = request.POST.get('price')
				fiesta.Lugar_id = id_place
				fiesta.precio = fiesta.precio + int(price)
				flag_place = True
				boda.precio = int(boda.precio) + int(price)
				boda.save()
				fiesta.save()
				mensaje_succes = (True , "Lugar para tu fiesta correctamente asignado")

			else:
				mensaje_error = (True , "Ya tienes un lugar asignado para tu fiesta")

		if value_btn == "add_foto":
			if fiesta.Fotos == False:
				flag_foto = True
				fiesta.Fotos=True
				fiesta.save()
				mensaje_succes = (True , "Fotos para tu fiesta correctamente agregadas")

			else:
				mensaje_error = (True , "Las fotos para tu fiesta ya fueron agregadas")

		if value_btn == "add_comida":
			cantidad_comida = request.POST.get('cantidad_comida')
			flag_comida = True
			id_comida = request.POST.get('id_comida')

			if int(id_comida) not in indices_alimentos:
				price = request.POST.get('price')
				comida_inst = Alimento.objects.filter(id__exact=id_comida)
				subtotal = (int(price) * int (cantidad_comida))
				comida = AlimentoCarrito(FiestaEvento = fiesta , Alimento = comida_inst[0], Cantidad = cantidad_comida, subtotal=subtotal)
				fiesta.precio = fiesta.precio + subtotal
				boda.precio = boda.precio + int(subtotal)
				boda.save()
				fiesta.save()
				comida.save()
				alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
				mensaje_succes = (True , "Alimento para tu fiesta correctamente agregado")
				indices_alimentos.clear()

				if alimento.count() > 0:
					for a in alimento:
						indices_alimentos.append(a.Alimento.id)

			else:
				mensaje_error = (True , "Este alimento ya fue agregado")

		if value_btn == "add_entretenimiento":
			flag_entre = True
			id_entre = request.POST.get('id_entretenimiento')
			price = request.POST.get('price')

			if int(id_entre) not in indices_entretenimientos:
				fiesta.precio = fiesta.precio + int(price)
				boda.precio = boda.precio + int(price)
				boda.save()	
				fiesta.save()
				entre_inst = Entretenimiento.objects.filter(id__exact=id_entre)
				entre = EntretenimientoCarrito(FiestaEvento = fiesta , Entretenimiento = entre_inst[0])
				entre.save()
				entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
				indices_entretenimientos.clear()
				mensaje_succes = (True , "Entretenimiento para tu fiesta correctamente agregado")

				if entretenimiento.count() > 0:
					for e in entretenimiento:
						indices_entretenimientos.append(e.Entretenimiento.id)

			else:
				mensaje_error = (True , "Este entretenimiento ya fue agregado")

		if value_btn == "delete_lugar":
			if flag_place == True:
				fiesta.Lugar = None
				price = request.POST.get('price')
				fiesta.precio = fiesta.precio - int(price)
				boda.precio = boda.precio - int(price)
				flag_place = False
				fiesta.save()
				boda.save()
				mensaje_delete = (True , "Lugar eliminado correctamente")
			else:
				mensaje_error = (True , "Este lugar ya fue eliminado")


		if value_btn == "delete_foto":
			if flag_foto == True:
				fiesta.Fotos=False
				flag_foto = False
				fiesta.save()
				mensaje_delete = (True , "Fotos eliminadas correctamente")
			else:
				mensaje_error = (True , "Las fotos ya fueron removidas")
			

		if value_btn == "delete_comida":
			comida_id = request.POST.get('comida_id')

			if int(comida_id) in indices_alimentos:
				alimento_carrito_id = request.POST.get('alimento_carrito_id')
				alimentocarrito = AlimentoCarrito.objects.filter(id__exact=alimento_carrito_id)
				cantidad = alimentocarrito[0].Cantidad
				subtotal = alimentocarrito[0].subtotal
				alimentocarrito.delete()
				alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
				indices_alimentos.clear()
				fiesta.precio = int(fiesta.precio) - (int(subtotal))
				boda.precio = boda.precio - int(subtotal)
				boda.save()
				fiesta.save()
				mensaje_delete = (True , "Alimento eliminado correctamente")

				if alimento.count() > 0:
					for a in alimento:
						indices_alimentos.append(a.Alimento.id)
			else:
				mensaje_error = (True , "Este alimento ya fue eliminado")

		if value_btn == "delete_entretenimiento":
			entretenimiento_id = request.POST.get('entretenimiento_id')

			if int(entretenimiento_id) in indices_entretenimientos:
				entretenimiento_carrito_id = request.POST.get('entretenimiento_carrito_id')
				entre = Entretenimiento.objects.get(id=entretenimiento_id)
				entretenimientocarrito = EntretenimientoCarrito.objects.filter(id__exact=entretenimiento_carrito_id)
				entretenimientocarrito.delete()

				entretenimiento = EntretenimientoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
				indices_entretenimientos.clear()
				price = request.POST.get('price')
				fiesta.precio = int(fiesta.precio) - int(price)
				boda.precio = boda.precio - int(price)
				boda.save()
				fiesta.save()
				mensaje_delete = (True , "Entrenimiento eliminado correctamente")

				if entretenimiento.count() > 0:
					for e in entretenimiento:
						indices_entretenimientos.append(e.Entretenimiento.id)
			else:
				mensaje_error = (True , "Este entretenimiento ya fue eliminado")


		Lugares = Lugar.objects.filter(tipo='fiesta')

		for indexLugar in range(0, len(Lugares)):
			precio = getPriceFormat(Lugares[indexLugar].precio)
			Lugares[indexLugar].precioSTR = precio

		if fiesta.Lugar:
			fiesta.Lugar.precioSTR = getPriceFormat(fiesta.Lugar.precio)

		for indexAlimento in range(0, len(Alimentos)):
			precio = getPriceFormat(Alimentos[indexAlimento].precio)
			Alimentos[indexAlimento].precioSTR = precio

		for food in alimento:
			precio = getPriceFormat(food.Alimento.precio)
			precioSub = getPriceFormat(food.subtotal)
			food.subtotal = precioSub
			food.Alimento.precioSTR = precio

		for indexEntre in range(0, len(Entretenimientos)):
			precio = getPriceFormat(Entretenimientos[indexEntre].precio)
			Entretenimientos[indexEntre].precioSTR = precio

		for entre in entretenimiento:
			precio = getPriceFormat(entre.Entretenimiento.precio)
			entre.Entretenimiento.precioSTR = precio

		size_alimentos = len(indices_alimentos)
		size_entre = len(indices_entretenimientos)
		limite = 0

		if size_alimentos > limite:
			flag_comida = True
		else:
			flag_comida = False

		if size_entre > limite:
			flag_entre = True
		else:
			flag_entre = False

		template = get_template('Fiesta/fiesta.html')
		context = {
			'Lugares' : Lugares,
			'flag_place' : flag_place,
			'flag_foto' : flag_foto,
			'flag_entre' : flag_entre,
			'flag_comida' : flag_comida,
			'fiesta' : fiesta,
			'alimento' : alimento,
			'Alimentos' : Alimentos,
			'indices_alimentos' : indices_alimentos,
			'entretenimiento' : entretenimiento,
			'Entretenimientos' : Entretenimientos,
			'indices_entretenimientos' : indices_entretenimientos,
			'mensaje' : mensaje_error,
			'mensaje_succes' : mensaje_succes,
			'mensaje_delete' : mensaje_delete,
			'precio' : getPriceFormat(fiesta.precio),
			'user_id': user_id,
			'boda_id': boda_id,
			'fiesta_id':fiesta_id,
			'ceremonia_id' : ceremonia.id,
			'enamoradoNombre': boda.Enamorado1,
			'enamoradoNombre2': boda.Enamorado2
		}
		return HttpResponse(template.render(context, request))
