from Domain.models import Boda
from Fiesta.models import FiestaEvento
from Pareja.models import Enamorado
from Ceremonia.models import CeremoniaEvento
from .models import LunaMielEvento
from Fiesta.utils import getPriceFormat;


def baseContext(request):

    # borrowed from pareja

    user = request.user
    enamorado = Enamorado.objects.get(User_id=user)
    boda = Boda.objects.filter(Enamorado1_id=enamorado.id)

    if len(boda) == 0:
        boda = Boda.objects.filter(Enamorado2_id=enamorado.id)

    boda = boda[0]
    fiesta = FiestaEvento.objects.filter(Boda_id=boda.id).first()
    ceremonia = CeremoniaEvento.objects.filter(Boda_id=boda.id).first()
    luna = LunaMielEvento.objects.filter(Boda_id=boda.id).first()
    precio_pareja = int(boda.Enamorado1.precio) + int(boda.Enamorado2.precio)
    print("user id ->", user.id)
    return {
        'user_id': user,
        'boda_id':boda.id,
        'fiesta_id':fiesta.id,
        'ceremonia_id':ceremonia.id,
        'enamorado': boda.Enamorado1,
        'enamorado2': boda.Enamorado2,
        'precio_pareja': getPriceFormat(precio_pareja),
        'precio_boda': getPriceFormat(boda.precio),
        'enamoradoNombre': boda.Enamorado1,
		'enamoradoNombre2': boda.Enamorado2,
        'luna':luna,
        'boda': boda
    }


def actualizarPrecio(request):
    ctx = baseContext(request)
    luna = ctx['luna']
    boda = ctx['boda']
    suma = 0
    for ac in luna.actividadcarrito_set.all():
        suma += ac.Actividad.precio*ac.cantidad

    for ac in luna.hotelcarrito_set.all():
        suma += ac.Hotel.precio*ac.cantidad
    precio_anterior = luna.precio
    luna.precio = suma
    luna.save()

    boda.precio += (luna.precio-precio_anterior)
    boda.save()
