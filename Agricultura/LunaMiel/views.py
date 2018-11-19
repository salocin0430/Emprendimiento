from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from .views import *
from .utils import baseContext,actualizarPrecio
from .models import *

# Create your views here.

@login_required(login_url='index')
def dashboardView(request):
    ctx = baseContext(request)
    actividades = Actividad.objects.all()
    hoteles = Hotel.objects.all()
    ctx['actividades'] = actividades
    ctx['hoteles'] = hoteles
    return render(request, 'LunaMiel/dashboard.html', ctx)

@login_required(login_url='index')
def post_actividad(request):
    if request.method == 'POST':
        ctx = baseContext(request)
        luna = ctx['luna']
        actividad = Actividad.objects.get(pk=request.POST['id'])
        if actividad is not None:
            try:
                cantidad = int(request.POST['cantidad'])
                if cantidad<1:
                    raise Exception()
                previa = luna.actividadcarrito_set.get(Actividad=actividad)
                previa.cantidad = cantidad
                previa.save()
            except ActividadCarrito.DoesNotExist:
                luna.actividadcarrito_set.create(Actividad=actividad,cantidad=request.POST['cantidad'])
            actualizarPrecio(request)
            return JsonResponse({
                'message':'ok'
            });


@login_required(login_url='index')
def delete_actividad(request,id):
    if request.method == 'DELETE':
        ctx = baseContext(request)
        luna = ctx['luna']
        actividad = Actividad.objects.get(pk=id)
        if actividad is not None:
            try:
                luna.actividadcarrito_set.filter(Actividad=actividad).delete()
            except ActividadCarrito.DoesNotExist:
                pass
            actualizarPrecio(request)
            return JsonResponse({
                'message': 'ok'
            })


@login_required(login_url='index')
def post_hotel(request):
    if request.method == 'POST':
        ctx = baseContext(request)
        luna = ctx['luna']
        hotel = Hotel.objects.get(pk=request.POST['id'])
        if hotel is not None:
            try:
                cantidad = int(request.POST['cantidad'])
                if cantidad < 1:
                    raise Exception()
                previa = luna.hotelcarrito_set.get(Hotel=hotel)
                previa.cantidad = cantidad
                previa.save()
            except HotelCarrito.DoesNotExist:
                luna.hotelcarrito_set.create(Hotel=hotel, cantidad=request.POST['cantidad'])
            actualizarPrecio(request)
            return JsonResponse({
                'message':'ok'
            });


@login_required(login_url='index')
def delete_hotel(request, id):
    if request.method == 'DELETE':
        ctx = baseContext(request)
        luna = ctx['luna']
        hotel = Hotel.objects.get(pk=id)
        if hotel is not None:
            try:
                luna.hotelcarrito_set.filter(Hotel=hotel).delete()
            except HotelCarrito.DoesNotExist:
                pass
            actualizarPrecio(request)
            return JsonResponse({
                'message': 'ok'
            })
