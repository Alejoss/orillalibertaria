from django.http import HttpResponse
from django.shortcuts import render

from perfiles.models import Perfiles
from models import Notificacion

# Create your views here.


def marcar_leidas(request):
    if request.is_ajax():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        notificaciones_marcar = Notificacion.objects.filter(
            target=perfil_usuario).order_by('-id')[:5]
        for notificacion in notificaciones_marcar:
            notificacion.leida = True
            notificacion.save()

    return HttpResponse("notificacion leidas")
