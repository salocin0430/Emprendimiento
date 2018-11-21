from django.http import HttpResponse
from django.template.loader import get_template
from Domain.models import Boda
from Domain.models import Lugar
from .models import FiestaEvento, AlimentoCarrito, Alimento, EntretenimientoCarrito, Entretenimiento
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
	boda2 = Boda.objects.get(Enamorado1_id=enamorado.id)
	

	if str(boda2.id) != str(boda_id):
		return redirect('tableroResumen')

	boda = Boda.objects.filter(id__exact=boda_id)
	fiesta = FiestaEvento.objects.get(Boda_id=boda_id)


	alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)
	indices_alimentos = []
	indices_entretenimientos = []
	mensaje_error = (False , "")
	mensaje_succes = (False , "")
	mensaje_delete = (False , "")
	subtotal = ""

	if str(fiesta_id) != str(fiesta.id):
		return redirect('tableroResumen')



	count_comida = AlimentoCarrito.objects.all()

	flag_comida = len(count_comida) > 0


	Fiesta = None
	if request.method == 'GET':
		Alimentos = Alimento.objects.all()
		alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)

		for indexAlimento in range(0, len(Alimentos)):
			precio = getPriceFormat(Alimentos[indexAlimento].precio)
			Alimentos[indexAlimento].precioSTR = precio

		for food in alimento:
			precio = getPriceFormat(food.Alimento.precio)
			precioSub = getPriceFormat(food.subtotal)
			food.subtotal = precioSub
			food.Alimento.precioSTR = precio



		indices_alimentos.clear()


		if alimento.count() > 0:
			for a in alimento:
				indices_alimentos.append(a.Alimento.id)


		if boda_id != 0:
			boda = Boda.objects.filter(id__exact=boda_id)

			template = get_template('Fiesta/fiesta.html')

		size_alimentos = len(indices_alimentos)
		limite = 0

		flag_comida = size_alimentos > limite
	

		context = {
			'flag_comida' : flag_comida,
			'fiesta' : fiesta,
			'alimento' : alimento,
			'Alimentos' : Alimentos,
			'indices_alimentos' : indices_alimentos,
			'precio' : getPriceFormat(fiesta.precio),
			'user_id': user_id,
			'boda_id': boda_id,
			'fiesta_id':fiesta_id,
			'enamoradoNombre': boda[0].Enamorado1
		}
		return HttpResponse(template.render(context, request))

	if request.method == 'POST':
		fiesta = FiestaEvento.objects.get(Boda_id=boda_id)
		boda = Boda.objects.get(id=boda_id)
		value_btn = request.POST.get('btn_value')
		Alimentos = Alimento.objects.all()
		alimento = AlimentoCarrito.objects.filter(FiestaEvento_id=fiesta.id)



		if alimento.count() > 0:
			indices_alimentos.clear()
			for a in alimento:
				indices_alimentos.append(a.Alimento.id)



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




		for indexAlimento in range(0, len(Alimentos)):
			precio = getPriceFormat(Alimentos[indexAlimento].precio)
			Alimentos[indexAlimento].precioSTR = precio

		for food in alimento:
			precio = getPriceFormat(food.Alimento.precio)
			precioSub = getPriceFormat(food.subtotal)
			food.subtotal = precioSub
			food.Alimento.precioSTR = precio




		size_alimentos = len(indices_alimentos)
		limite = 0

		if size_alimentos > limite:
			flag_comida = True
		else:
			flag_comida = False


		template = get_template('Fiesta/fiesta.html')
		context = {
			'flag_comida' : flag_comida,
			'fiesta' : fiesta,
			'alimento' : alimento,
			'Alimentos' : Alimentos,
			'indices_alimentos' : indices_alimentos,
			'mensaje' : mensaje_error,
			'mensaje_succes' : mensaje_succes,
			'mensaje_delete' : mensaje_delete,
			'precio' : getPriceFormat(fiesta.precio),
			'user_id': user_id,
			'boda_id': boda_id,
			'fiesta_id':fiesta_id,
			'enamoradoNombre': boda.Enamorado1
		}
		return HttpResponse(template.render(context, request))
