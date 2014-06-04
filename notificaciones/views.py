from django.http import HttpResponse
from django.shortcuts import render

from endless_pagination.decorators import page_template

from perfiles.models import Perfiles
from temas.models import Temas, Posts
from models import Notificacion
from olibertaria.utils import obtener_args_notificacion, obtener_num_notificaciones


def marcar_leidas(request):
    #Marca las 5 ultimas notificaciones como leidas
    if request.is_ajax():
        cantidad = request.GET.get('cantidad', '')
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

        if cantidad == 'todos':
            notificaciones_marcar = Notificacion.objects.filter(target=perfil_usuario, leida=False)
        else:
            notificaciones_marcar = Notificacion.objects.filter(
                target=perfil_usuario).order_by('-id')[:5]

        for notificacion in notificaciones_marcar:
            notificacion.leida = True
            notificacion.save()

        return HttpResponse("notificacion leidas")
    else:
        return HttpResponse("notificaciones_leidas_error")


@page_template('index_page_notificaciones.html')
def notificaciones_index(request, template='notificaciones/notificaciones_index.html', extra_context=None):
    #muestra todas las notificaciones.
    # Datos del usuario
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    puntos_recibidos = perfil_usuario.votos_recibidos
    num_posts = Posts.objects.filter(creador=perfil_usuario).count()
    num_temas = Temas.objects.filter(creador=perfil_usuario).count()
    creo_temas = False
    temas_usuario = []
    if num_temas > 0:
        temas_usuario = Temas.objects.filter(creador=perfil_usuario)
        creo_temas = True

    #Notificaciones
    notificaciones_obj = Notificacion.objects.filter(target=perfil_usuario).order_by('-id')
    lista_notificaciones = []
    for n in notificaciones_obj:
        notificacion_args = obtener_args_notificacion(n)
        lista_notificaciones.append(notificacion_args)

    num_notificaciones = obtener_num_notificaciones(perfil_usuario)

    context = {'num_notificaciones': num_notificaciones, 'lista_notificaciones': lista_notificaciones,
               'puntos_recibidos': puntos_recibidos, 'num_posts': num_posts, 'num_temas': num_temas,
               'creo_temas': creo_temas, 'temas_usuario': temas_usuario}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
