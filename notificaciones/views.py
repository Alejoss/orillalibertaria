# -*- coding: utf-8 -*-
# VIEWS NOTIFICACIONES

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template

from perfiles.models import Perfiles
from temas.models import Temas, Posts
from models import Notificacion
from olibertaria.utils import obtener_args_notificacion, obtener_num_notificaciones


@login_required
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


@login_required
def marcar_leida_redirect(request, object_id, slug):
    #Marca una notificacion como leida y redirige a la pagina del objeto de la notificacion.
    notificacion = Notificacion.objects.get(id=object_id)
    if notificacion.leida is False:
        notificacion.leida = True
        notificacion.save()
    tipo_objeto = notificacion.tipo_objeto
    objeto_id = notificacion.objeto_id
    if tipo_objeto == "post":
        return redirect('temas:post', slug=slug, post_id=objeto_id, queryset='recientes')
    elif tipo_objeto == "video":
        return redirect('videos:video', slug=slug, video_id=objeto_id)
    elif tipo_objeto == "cita":
        return redirect('citas:cita', cita_id=objeto_id)
    elif tipo_objeto == "imagen":
        return redirect('imagenes:imagen', imagen_id=objeto_id)
    else:
        return redirect('temas:main', queryset='activos')


@login_required
@page_template('index_page_notificaciones.html')
def notificaciones_index(request, template='notificaciones/notificaciones_index.html', extra_context=None):
    #muestra todas las notificaciones.
    # Datos del usuario
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    avatar_large = "%s?type=large" % (perfil_usuario.imagen_perfil)
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
               'creo_temas': creo_temas, 'temas_usuario': temas_usuario, 'avatar_large': avatar_large}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)
