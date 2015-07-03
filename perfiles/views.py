# -*- coding: utf-8 -*-
# VIEWS PERFILES

import random

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template

from forms import PerfilesForm
from models import Perfiles
from olibertaria.utils import obtener_cita, obtener_imagen_tema,\
                            obtener_respuestas_post, obtener_avatar_large,\
                            obtener_args_post
from temas.utils import obtener_posts_recientes
from temas.models import Temas
from temas.models import Posts, Respuestas, Votos
from videos.models import Videos, VFavoritos
from citas.models import Cfavoritas, Cita
from imagenes.models import Ifavoritas, Imagen
from utils import obtener_links_perfil, obtener_num_favoritos

# print "nombre variable: %s" %(nombre variable) -- print para debug una variable


# Ajax
def revisar_nickname(request):
    # Evita que un usuario elija un nickname que ya existe
    if request.is_ajax():
        nickname_nuevo = request.GET.get('nickname', '')
        if Perfiles.objects.exclude(usuario=request.user).filter(nickname=nickname_nuevo).exists():
            return HttpResponse("false")
        else:
            return HttpResponse("true")
    else:
        return HttpResponseRedirect(reverse('perfiles:login'))


def login_page(request):
    # Custom login. Facebook + Twitter + Google
    template = 'perfiles/login.html'

    #temas - posts populares
    posts_populares = obtener_posts_recientes(3)
    imagenes_posts_populares = []
    for post in posts_populares:
        imagen = obtener_imagen_tema(post.tema)
        imagenes_posts_populares.append(imagen)

    #citas
    citas = []
    citas_obj = Cita.objects.filter(eliminada=False).order_by('-favoritos_recibidos')[:6]
    for c in citas_obj:
        cita = obtener_cita(c)
        citas.append(cita)

    #imagenes
    imagenes_display_obj = Imagen.objects.filter(eliminada=False).order_by('-favoritos_recibidos')[:5]
    imagenes_display = []
    for i in imagenes_display_obj:
        imagenes_display.append(i.url)

    context = {'imagenes_display': imagenes_display, 'posts_populares': posts_populares,
               'imagenes_posts_populares': imagenes_posts_populares, 'citas': citas}

    return render(request, template, context)


def authcheck(request):
    # standard auth de Django. Para usuarios especiales
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return redirect('temas:main', 'activos')
    else:
        return redirect('perfiles:login')


def logout(request):
    auth.logout(request)  # Logout el user guardado en Request
    return redirect('temas:main', 'activos')


@login_required
def editar_perfil_des(request):
    template = 'perfiles/editar_perfil_des.html'

    user = request.user
    # obtiene/crea un model de Perfiles para el user
    perfil_usuario, created = Perfiles.objects.get_or_create(usuario=user)
    tiene_imagenesfav = Ifavoritas.objects.filter(
        perfil=perfil_usuario).exists()
    tiene_frasesfav = Cfavoritas.objects.filter(perfil=perfil_usuario).exists()
    descripcion = perfil_usuario.obtener_descripcion()
    avatar_large = obtener_avatar_large(perfil_usuario)

    if request.method == 'POST':
        form = PerfilesForm(request.POST)
        if form.is_valid():

            # editar User model
            user.email = form.cleaned_data.get('email')
            user.save()

            # editar Perfiles model
            nickname = form.cleaned_data.get('nickname')
            if len(nickname) < 1:
                # si no tiene un nickname válido, se crea uno automáticamente
                rand_num = random.randint(99)
                nickname = "%s_nick_%s" % (user.username, rand_num)

            perfil_usuario.nickname = nickname
            perfil_usuario.descripcion = form.cleaned_data.get('descripcion')
            # guarda los links en lowercase
            perfil_usuario.link1 = (form.cleaned_data.get('link1')).lower()
            perfil_usuario.link2 = (form.cleaned_data.get('link2')).lower()
            perfil_usuario.link3 = (form.cleaned_data.get('link3')).lower()
            perfil_usuario.link4 = (form.cleaned_data.get('link4')).lower()
            perfil_usuario.link5 = (form.cleaned_data.get('link5')).lower()
            perfil_usuario.save()
            return redirect('perfiles:perfil', username=request.user.username, queryset='recientes')

    editar_perfil_form = PerfilesForm(initial={
        'email': user.email,
        'descripcion': descripcion,
        'nickname': perfil_usuario.nickname,
        'link1': perfil_usuario.link1, 'link2': perfil_usuario.link2,
        'link3': perfil_usuario.link3, 'link4': perfil_usuario.link4,
        'link5': perfil_usuario.link5})

    context = {'editar_perfil_form': editar_perfil_form,
               'tiene_imagenesfav': tiene_imagenesfav,
               'tiene_frasesfav': tiene_frasesfav,
               'avatar_large': avatar_large}

    return render(request, template, context)


@page_template('index_page_perfiles.html')
def perfil(request, username, queryset, template="perfiles/perfil.html",
           extra_context=None):
    # recibe un username y un queryset.
    usuario_visitado = get_object_or_404(User, username=username)  # usuario dueño del perfil
    perfil_usuario = get_object_or_404(Perfiles, usuario=usuario_visitado)
    propio_usuario = False
    perfil_usuario_visitante = None
    if request.user.is_authenticated():
        perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)
        if perfil_usuario == perfil_usuario_visitante:
            propio_usuario = True

    # Datos del usuario
    avatar_large = obtener_avatar_large(perfil_usuario)

    nombre_completo = usuario_visitado.get_full_name()
    descripcion = perfil_usuario.obtener_descripcion()
    num_favoritos = obtener_num_favoritos(perfil_usuario)
    num_temas = Temas.objects.filter(creador=perfil_usuario).count()
    creo_temas = False
    temas_usuario = []
    if num_temas > 0:
        temas_usuario = Temas.objects.filter(creador=perfil_usuario).order_by('nombre')
        creo_temas = True

    # Si el queryset es "videos" entonces toma los videos del usuario, si no, toma los posts. 
    posts = []            
    videos = []
    if queryset == "videos":
        videos_obj = Videos.objects.filter(perfil=perfil_usuario, eliminado=False).order_by("-fecha")

        if perfil_usuario_visitante:
            videos_favoritos_visitante_obj = VFavoritos.objects.filter(perfil=perfil_usuario_visitante, eliminado=False)
            videos_favoritos_visitante = []
            for vfav in videos_favoritos_visitante_obj:
                videos_favoritos_visitante.append(vfav.video)

        for video in videos_obj:
            # Suma la clase a los videos favoritos        
            if request.user.is_authenticated():
                if video in videos_favoritos_visitante:
                    es_favorito = "es_favorito"
                else:
                    es_favorito = "no_es_favorito"
            else:
                es_favorito = "no_es_favorito"

            if video.es_youtube is True:
                imagen_video = "http://img.youtube.com/vi/%s/0.jpg" % (video.youtube_id)
            else:
                imagen_video = "http://www.flaticon.es/png/256/24933.png"

            num_respuestas_video = Posts.objects.filter(video=video, eliminado=False).count()
            videos.append([video, imagen_video, es_favorito, num_respuestas_video])

    else:    
        posts_obj = Posts.objects.filter(creador=perfil_usuario, eliminado=False).order_by("-fecha")
        for p in posts_obj:

            # [post, voted_status, num_respuestas, texto_procesado, hora_procesada]
            post = obtener_args_post(p, perfil_usuario_visitante)

            # Sumar post_en_video, usuario_respuesta, respuestas_post
            post_en_video = False
            if p.video is not None:
                # si el post pertenece a un video
                post_en_video = True

            if p.es_respuesta is True:
                # informacion sobre el post padre
                if Respuestas.objects.filter(post_respuesta=p).exists():
                    respuesta = Respuestas.objects.get(post_respuesta=p)
                    usuario_respuesta = respuesta.post_padre.creador.nickname
                else:
                    # Por si de dan respuestas descuadradas (respuestas sin post padre)
                    usuario_respuesta = None
            else:
                usuario_respuesta = None

            respuestas_post = obtener_respuestas_post(p)

            post.extend([post_en_video, usuario_respuesta, respuestas_post])

            #suma el post a la lista de posts
            posts.append(post)

    # cita
    if num_favoritos[1] == 0:
        cita_favorita = None
    else:
        citas_favoritas_obj = Cfavoritas.objects.filter(
            perfil=perfil_usuario, eliminado=False)
        cita_favorita_obj = (random.choice(citas_favoritas_obj)).cita
        cita_favorita = obtener_cita(cita_favorita_obj)

    # imagenes
    portada = ""
    imagenes_favoritas = []

    if num_favoritos[0] > 0:
        if num_favoritos[0] > 3:
            # Limita a 3 las imagenes del display de portada
            imagenes_display = 3
        else:
            imagenes_display = num_favoritos[0]

        ifavoritas_objects = Ifavoritas.objects.filter(
            perfil=perfil_usuario, eliminado=False, portada=False).order_by('-fecha')[:imagenes_display]
        for i in ifavoritas_objects:
            imagenes_favoritas.append(i.imagen.url)

        if Ifavoritas.objects.filter(perfil=perfil_usuario, eliminado=False, portada=True).exists():
            portada_obj = Ifavoritas.objects.get(
                perfil=perfil_usuario, eliminado=False, portada=True)
        else:
            portada_obj = Ifavoritas.objects.filter(
                perfil=perfil_usuario, eliminado=False).latest('id')
        portada = portada_obj.imagen.url

    # links
    links = obtener_links_perfil(perfil_usuario)

    context = {
        'portada': portada, 'usuario_visitado': usuario_visitado, 'avatar_large': avatar_large,
        'nombre_completo': nombre_completo, 'links': links, 'descripcion': descripcion,
        'posts': posts, 'cita_favorita': cita_favorita, 'imagenes_favoritas': imagenes_favoritas,
        'num_favoritos': num_favoritos, 'num_temas': num_temas,
        'temas_usuario': temas_usuario, 'queryset': queryset,
        'creo_temas': creo_temas, 'videos': videos,
        'perfil_usuario': perfil_usuario, 'propio_usuario': propio_usuario}

    if extra_context is not None:  # endless pagination
        context.update(extra_context)

    return render(request, template, context)


def postsfav(request, username):
    template = "perfiles/postsfav.html"
    usuario_fav = get_object_or_404(User, username=username)
    perfil_usuario = get_object_or_404(Perfiles, usuario=usuario_fav)
    num_favoritos = obtener_num_favoritos(perfil_usuario)
    propio_usuario = False
    perfil_usuario_visitante = None
    if request.user.is_authenticated():
        perfil_usuario_visitante = get_object_or_404(Perfiles, usuario=request.user)
        if request.user == usuario_fav:
            propio_usuario = True

    # Posts
    posts = []
    votos_posts = Votos.objects.filter(tipo=1, usuario_votante=perfil_usuario,
                                       post_votado__es_respuesta=False,
                                       post_votado__eliminado=False).order_by('-id')

    for p in votos_posts:
        post_votado = p.post_votado
        post_args = obtener_args_post(post_votado, perfil_usuario_visitante)
        post_en_video = False
        if post_votado.video is not None:
            # si el post pertenece a un video
            post_en_video = True
        post_args.extend([post_en_video])
        posts.append(post_args)

    context = {'perfil_usuario': perfil_usuario, 'posts': posts,
               'num_favoritos': num_favoritos, 'propio_usuario': propio_usuario}

    return render(request, template, context)


def allyoutouch(request):
    return render(request, 'perfiles/allyoutouchlogin.html')
