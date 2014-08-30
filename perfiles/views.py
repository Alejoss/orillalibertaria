# -*- coding: utf-8 -*-
# VIEWS PERFILES

import random

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template

from forms import FormRegistroUsuario, PerfilesForm
from models import Perfiles
from olibertaria.utils import obtener_voted_status, obtener_cita, procesar_espacios, tiempo_desde, \
    obtener_imagen_tema
from temas.utils import obtener_posts_populares
from temas.models import Temas
from temas.models import Posts, Respuestas
from citas.models import Cfavoritas, Cita
from videos.models import VFavoritos
from imagenes.models import Ifavoritas, Imagen
from utils import obtener_links_perfil

# print "nombre variable: %s" %(nombre variable) -- print para debug una variable
# Create your views here.


def revisar_nickname(request):
    if request.is_ajax():
        print "llego ajax revisar_nickname"
        nickname_nuevo = request.GET.get('nickname', '')
        print nickname_nuevo
        if Perfiles.objects.exclude(usuario=request.user).filter(nickname=nickname_nuevo).exists():
            print "False"
            return HttpResponse("false")
        else:
            print "True"
            return HttpResponse("true")
    else:
        return HttpResponseRedirect(reverse('perfiles:login'))


def login_page(request):
    # Custom login. Facebook + Twitter.
    template = 'perfiles/login.html'

    #temas - posts populares
    posts_populares = obtener_posts_populares(5)
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
    # standard auth de Django.
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    # busca en la bd User uno que existe con ese usuario y password
    if user is not None:
        # Si existe, hace login a ese usuario y lo guarda en "request"
        auth.login(request, user)
        return redirect('temas:main', 'recientes')
    else:
        return redirect('perfiles:login')


def logout(request):
    auth.logout(request)  # Logout el user guardado en Request
    return redirect('temas:main', 'recientes')


def registrar(request):
    template = 'perfiles/registrar.html'
    # Registra nuevos usuarios.
    # Hay que eliminar esta variable y cambiar por los errors del form.
    error = ""
    if request.method == 'POST':
        # Recoge el form de forms.py y le asigna las variables del
        # diccionario de request.POST
        form = FormRegistroUsuario(request.POST)
        # valida el form conforme a las reglas preestablecidas en form.py
        if form.is_valid():
            form.save()  # Guarda los valores en la base de datos auth.User.
            user = User.objects.get(username=form.cleaned_data['username'])
            perfil_nuevo, created = Perfiles.objects.get_or_create(
                usuario=user)
            perfil_nuevo.save()
            return HttpResponseRedirect(reverse('temas:main', kwargs={'queryset': u'recientes'}))
        else:
            error = "error en form.is_valid"  # !!!
    # Crea un nuevo form vacio. (unbound)
    user_creation_form = FormRegistroUsuario()
    context = {'user_creation_form': user_creation_form, 'error': error}
    return render(request, template, context)


def registro_ok(request):

    # Lleva a una página de Bienvenida.
    context = {}
    return render(request, 'perfiles/registro_ok.html', context)


@login_required
def editar_perfil_des(request):
    template = 'perfiles/editar_perfil_des.html'
    print "llego editar_perfil_des"

    user = request.user
    # crea una tabla de Perfiles para el user
    # si no existe una ya y obtiene esa tabla como "obj"
    perfil_usuario, created = Perfiles.objects.get_or_create(usuario=user)
    tiene_imagenesfav = Ifavoritas.objects.filter(
        perfil=perfil_usuario).exists()
    tiene_frasesfav = Cfavoritas.objects.filter(perfil=perfil_usuario).exists()
    descripcion = perfil_usuario.obtener_descripcion()

    if request.method == 'POST':
        form = PerfilesForm(request.POST)
        if form.is_valid():
            print "form is valid"
            # Llena los valores del obj con los valores del form request.Post.
            user.email = form.cleaned_data.get('email')
            user.save()

            nickname = form.cleaned_data.get('nickname')
            if len(nickname) < 1:
                nickname = "%s_nickname" % (user.first_name)
            perfil_usuario.nickname = nickname
            perfil_usuario.descripcion = form.cleaned_data.get('descripcion')
            perfil_usuario.link1 = (form.cleaned_data.get('link1')).lower()
            perfil_usuario.link2 = (form.cleaned_data.get('link2')).lower()
            perfil_usuario.link3 = (form.cleaned_data.get('link3')).lower()
            perfil_usuario.link4 = (form.cleaned_data.get('link4')).lower()
            perfil_usuario.link5 = (form.cleaned_data.get('link5')).lower()
            perfil_usuario.save()
            return redirect('perfiles:perfil', username=request.user.username, queryset='recientes')
        else:
            print "form not valid"

    editar_perfil_form = PerfilesForm(initial={
        'email': user.email,
        'descripcion': perfil_usuario.descripcion,
        'nickname': perfil_usuario.nickname,
        'link1': perfil_usuario.link1, 'link2': perfil_usuario.link2,
        'link3': perfil_usuario.link3, 'link4': perfil_usuario.link4,
        'link5': perfil_usuario.link5})

    context = {'editar_perfil_form': editar_perfil_form,
               'tiene_imagenesfav': tiene_imagenesfav,
               'tiene_frasesfav': tiene_frasesfav,
               'descripcion': descripcion}

    return render(request, template, context)


@page_template('index_page_perfiles.html')
def perfil(request, username, queryset, template="perfiles/perfil.html",
           extra_context=None):
    # recibe del urlpattern un username y un queryset.
    usuario_user = User.objects.get(username=username)
    usuario_perfil = Perfiles.objects.get(usuario=usuario_user)
    if request.user.is_authenticated():
        perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)

    # Datos del usuario
    avatar_large = None
    if usuario_perfil.imagen_perfil is not None:
        if "facebook" in usuario_perfil.imagen_perfil:
            avatar_large = "%s?type=large" % (usuario_perfil.imagen_perfil)
        elif "twimg" in usuario_perfil.imagen_perfil:
            avatar_large = (usuario_perfil.imagen_perfil).replace("_normal", "")
    else:
        avatar_large = "no tiene avata larga, remplazar"

    nombre_completo = usuario_user.get_full_name()
    puntos_recibidos = usuario_perfil.votos_recibidos
    num_posts = Posts.objects.filter(creador=usuario_perfil).count()
    num_temas = Temas.objects.filter(creador=usuario_perfil).count()
    creo_temas = False
    temas_usuario = []
    if num_temas > 0:
        temas_usuario = Temas.objects.filter(creador=usuario_perfil).order_by('nombre')
        creo_temas = True
    num_frases_favoritas = Cfavoritas.objects.filter(
        perfil=usuario_perfil).count()
    numero_imgfavoritas = 0
    usuario_fav = usuario_user.username
    descripcion = usuario_perfil.obtener_descripcion()
    nickname_perfil = usuario_perfil.nickname

    # Posts del usuario, utiliza el queryset de la URL: 'recientes' o 'populares'
    recientes = ""
    populares = ""
    q = ""
    if queryset == "populares":
        q = "-votos_total"
        populares = "active"
    else:
        q = "-fecha"
        recientes = "active"

    posts_obj = Posts.objects.filter(
        creador=usuario_perfil, eliminado=False).order_by(q)
    posts = []
    for p in posts_obj:
        post = [p]
        num_respuestas = Respuestas.objects.filter(post_padre=p).count()
        if p.es_respuesta is True:
            if Respuestas.objects.filter(post_respuesta=p).exists():
                respuesta = Respuestas.objects.get(post_respuesta=p)
                usuario_respuesta = respuesta.post_padre.creador.nickname
                post.extend([True, usuario_respuesta])
            else:
                # !!! Prueba para ver respuestas descuadradas (respuestas sin post padre)
                post.extend([False, ""])
        else:
            post.extend([False, ""])

        if request.user.is_authenticated():
            voted_status = obtener_voted_status(p, perfil_usuario_visitante)
        else:
            voted_status = "no-vote"
        post_en_video = False
        if p.video is not None:
            post_en_video = True

        texto_procesado = procesar_espacios(p.texto)
        hora_procesada = tiempo_desde(p.fecha)

        post.append(voted_status)
        post.append(num_respuestas)
        post.append(post_en_video)
        post.append(texto_procesado)
        post.append(hora_procesada)

        #suma el post a la lista de posts
        posts.append(post)

    # cita
    if num_frases_favoritas == 0:
        cita_favorita = ""
    else:
        citas_favoritas_obj = Cfavoritas.objects.filter(
            perfil=usuario_perfil, eliminado=False)
        cita_favorita_obj = (random.choice(citas_favoritas_obj)).cita
        cita_favorita = obtener_cita(cita_favorita_obj)

    # videos
    num_videos_favoritos = VFavoritos.objects.filter(
        perfil=usuario_perfil, eliminado=False).count()

    # imagenes
    portada = ""
    imagenes_favoritas = []
    tiene_imagenesfav = Ifavoritas.objects.filter(
        perfil=usuario_perfil, eliminado=False).exists()

    if tiene_imagenesfav:
        numero_imgfavoritas = Ifavoritas.objects.filter(
            perfil=usuario_perfil, eliminado=False).count()
        if numero_imgfavoritas > 3:
            imagenes_display = 3
        else:
            imagenes_display = numero_imgfavoritas
        ifavoritas_objects = Ifavoritas.objects.filter(
            perfil=usuario_perfil, eliminado=False, portada=False).order_by('-fecha')[:imagenes_display]
        for i in ifavoritas_objects:
            imagenes_favoritas.append(i.imagen.url)

        if Ifavoritas.objects.filter(perfil=usuario_perfil, portada=True).exists():
            portada_obj = Ifavoritas.objects.get(
                perfil=usuario_perfil, eliminado=False, portada=True)
        else:
            portada_obj = Ifavoritas.objects.filter(
                perfil=usuario_perfil, eliminado=False).latest('id')
        portada = portada_obj.imagen.url

    # links
    links = obtener_links_perfil(usuario_perfil)

    context = {
        'portada': portada, 'usuario_user': usuario_user, 'avatar_large': avatar_large,
        'nombre_completo': nombre_completo, 'links': links, 'descripcion': descripcion,
        'posts': posts, 'cita_favorita': cita_favorita, 'imagenes_favoritas': imagenes_favoritas,
        'usuario_fav': usuario_fav, 'tiene_imagenesfav': tiene_imagenesfav, 'recientes': recientes,
        'populares': populares, 'puntos_recibidos': puntos_recibidos, 'num_posts': num_posts,
        'num_temas': num_temas, 'numero_imgfavoritas': numero_imgfavoritas,
        'num_frases_favoritas': num_frases_favoritas, 'temas_usuario': temas_usuario,
        'creo_temas': creo_temas, 'num_videos_favoritos': num_videos_favoritos,
        'nickname_perfil': nickname_perfil}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def index(request):
    template = 'perfiles/index.html'
    # pagina principal de usuarios. Muestra los usuarios.
    # En el futuro mostrar actividad
    usuarios = Perfiles.objects.all()
    return render(request, template, {'usuarios': usuarios})
