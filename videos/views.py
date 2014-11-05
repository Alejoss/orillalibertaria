# -*- coding: utf-8 -*-
# VIEWS VIDEOS

import urlparse

from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from endless_pagination.decorators import page_template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from perfiles.models import Perfiles
from forms import FormNuevoVideo, FormEditarVideo
from temas.forms import FormNuevoPost
from models import Videos, VFavoritos, VDenunciados
from temas.models import Temas, Tema_descripcion, Posts, Respuestas
from citas.models import Cita
from notificaciones.models import Notificacion
from olibertaria.utils import obtener_imagen_tema, obtener_voted_status, procesar_espacios,\
    bersuit_vergarabat, tiempo_desde, obtener_respuestas_post, obtener_args_post
from perfiles.utils import obtener_num_favoritos
from temas.utils import popularidad_actividad_tema


@login_required
def nuevo_video(request, slug):
    # suma un video a un tema
    template = 'videos/nuevo.html'
    tema = get_object_or_404(Temas, slug=slug)
    if request.method == 'POST':
        form = FormNuevoVideo(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            url_data = urlparse.urlparse(url)  # para analizar la url, determinar donde esta hosteado el video
            query = urlparse.parse_qs(url_data.query)
            network_location = url_data.netloc
            youtube_id = ""
            if network_location in ("www.youtube.com", "youtube.com"):
                es_youtube = True
                youtube_id = query['v'][0]  # guarda el youtube ID.
            else:
                es_youtube = False

            # Crea un nuevo video object
            nuevo_video = Videos(
                tema=tema, perfil=perfil_usuario, titulo=titulo,
                descripcion=descripcion, url=url, es_youtube=es_youtube, youtube_id=youtube_id)
            nuevo_video.save()

            # calcular nivel actividad y de popularidad del Tema
            popularidad_actividad_tema(tema, "positivo")

            return redirect('videos:videos_tema', slug=tema.slug, queryset='recientes')
        else:
            print "form invalid"
            return redirect('videos:nuevo_video', slug=tema.slug)
    else:
        form_nuevo_video = FormNuevoVideo()

        # honeypot
        lista_bersuit = bersuit_vergarabat()

        context = {'form_nuevo_video': form_nuevo_video, 'tema': tema, 'lista_bersuit': lista_bersuit}
        return render(request, template, context)


@login_required
def editar_video(request, video_id):
    template = 'videos/editar_video.html'
    video = get_object_or_404(Videos, id=video_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if video.perfil == perfil_usuario:
        if request.method == "POST":
            form = FormEditarVideo(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                titulo = form.cleaned_data['titulo']
                descripcion = form.cleaned_data['descripcion']
                # Analiza el url del video y encuentra si viene de Youtube
                url_data = urlparse.urlparse(url)
                query = urlparse.parse_qs(url_data.query)
                network_location = url_data.netloc
                youtube_id = ""
                if network_location in ("www.youtube.com", "youtube.com"):
                    es_youtube = True
                    youtube_id = query['v'][0]
                else:
                    es_youtube = False
                video.url = url
                video.titulo = titulo
                video.descripcion = descripcion
                video.youtube_id, video.es_youtube = youtube_id, es_youtube
                video.save()
                return redirect('videos:video', video_id=video.id, slug=video.tema.slug, queryset='recientes')
        else:
            # honeypot
            lista_bersuit = bersuit_vergarabat()
            form_editar_video = FormEditarVideo(initial={'url': video.url, 'titulo': video.titulo,
                                                         'descripcion': video.descripcion})
            context = {'video': video, 'form_editar_video': form_editar_video, 'lista_bersuit': lista_bersuit}
            return render(request, template, context)
    else:
        raise Http404


@page_template('index_page_videos.html')
def videos_tema(request, slug, queryset, template='videos/videos_tema.html', extra_context=None):
    # La pagina del tema con la lista de videos.
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # Tema
    tema_obj = Temas.objects.get(slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
        descripcion_tema = procesar_espacios(descripcion_tema)
    else:
        descripcion_tema = "No tiene descripción por el momento"

    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count]

    # Videos, ordenados por el queryset
    populares = ""
    recientes = ""
    if queryset == "populares":
        q = "-favoritos_recibidos"
        populares = "active"
    else:
        q = '-id'
        recientes = "active"

    videos = []
    videos_obj = Videos.objects.filter(
        tema=tema_obj, eliminado=False).order_by(q)

    # Obtiene los videos favoritos del usuario
    if request.user.is_authenticated():
        videos_favoritos_obj = VFavoritos.objects.filter(
            perfil=perfil_usuario, eliminado=False)
        videos_favoritos_ids = []
        for v in videos_favoritos_obj:
            videos_favoritos_ids.append(int(v.video.id))

    for video in videos_obj:
        if video.es_youtube is True:
            imagen_video = "http://img.youtube.com/vi/%s/0.jpg" % (video.youtube_id)
        else:
            imagen_video = "http://www.flaticon.es/png/256/24933.png"

        es_favorito = "no_es_favorito"
        # Marca los videos favoritos con la clase "es_favorito"
        if request.user.is_authenticated():
            if video.id in videos_favoritos_ids:
                es_favorito = "es_favorito"

        num_respuestas_video = Posts.objects.filter(
            video=video, eliminado=False, es_respuesta=False).count()

        descripcion_video = procesar_espacios(video.descripcion)
        hora_procesada = tiempo_desde(video.fecha)

        videos.append([video, imagen_video, es_favorito, num_respuestas_video,
                       descripcion_video, hora_procesada])

    # cita sidebar
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    context = {'tema': tema, 'populares': populares, 'recientes': recientes,
               'videos': videos, 'cita': cita}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@page_template('index_page_videos_favoritos.html')
def videos_perfil(request, username, template="videos/videos_perfil.html", extra_context=None):
    # View para la pagina de videos favoritos del usuario
    user_object = get_object_or_404(User, username=username)
    perfil_usuario = get_object_or_404(Perfiles, usuario=user_object)
    propio_usuario = False
    num_favoritos = obtener_num_favoritos(perfil_usuario)
    if request.user.is_authenticated():
        perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)
        if perfil_usuario == perfil_usuario_visitante:
            propio_usuario = True  # usuario visitando sus propios videos favoritos
        else:
            propio_usuario = False

    # Videos
    videos_favoritos_obj = VFavoritos.objects.filter(
        perfil=perfil_usuario, eliminado=False)
    videos_obj = []
    for v in videos_favoritos_obj:
        videos_obj.append(v.video)
    videos = []

    # Obtiene lista de videos favoritos del usuario visitante
    if not propio_usuario:
        if request.user.is_authenticated():
            videos_favoritos_visitante_obj = VFavoritos.objects.filter(perfil=perfil_usuario_visitante,
                                                                       eliminado=False)
            videos_favoritos_visitante = []
            for v in videos_favoritos_visitante_obj:
                videos_favoritos_visitante.append(v.video)

    for video in videos_obj:
        # Suma la clase a los videos favoritos
        if propio_usuario:
            es_favorito = "es_favorito"
        else:
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

        num_respuestas_video = Posts.objects.filter(
            video=video, eliminado=False).count()
        videos.append([video, imagen_video, es_favorito, num_respuestas_video])

    # cita
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    context = {'videos': videos, 'perfil_usuario': perfil_usuario,
               'propio_usuario': propio_usuario, 'cita': cita,
               'num_favoritos': num_favoritos}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def video(request, video_id, slug, queryset):
    # Pagina del video.
    template = 'videos/video.html'
    perfil_usuario = None
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # Video
    video = Videos.objects.get(id=video_id)
    es_favorito = "no_es_favorito"
    propio_video = False
    if request.user.is_authenticated():
        if video.perfil == perfil_usuario:
            propio_video = True
        if VFavoritos.objects.filter(video=video, perfil=perfil_usuario, eliminado=False).exists():
            es_favorito = "es_favorito"

    origen_no_youtube = ""
    if video.es_youtube is False:
        if "vimeo.com" in video.url:
            origen_no_youtube = "vimeo"
        elif "ted.com" in video.url:
            origen_no_youtube = "ted"
    descripcion_video = procesar_espacios(video.descripcion)
    hora_procesada_video = tiempo_desde(video.fecha)

    # Tema
    tema_obj = Temas.objects.get(slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (
            Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
        descripcion_tema = procesar_espacios(descripcion_tema)
    else:
        descripcion_tema = "No tiene descripción por el momento"
    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

    # Posts en el video
    num_respuestas_video = Posts.objects.filter(
        video=video, eliminado=False, es_respuesta=False).count()
    populares = ""
    recientes = ""
    if queryset == "populares":
        q = "-votos_total"
        populares = "subrayar"
    else:
        q = "-id"
        recientes = "subrayar"

    posts_obj = Posts.objects.filter(video=video, eliminado=False, es_respuesta=False).order_by(q)
    posts = []
    for post in posts_obj:
        # Post
        p = obtener_args_post(post, perfil_usuario)
        respuestas_post = obtener_respuestas_post(post)
        p.append(respuestas_post)
        posts.append(p)

    # cita
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    # form_respuesta, mismo form que usa un post normal
    form_respuesta = FormNuevoPost()

    context = {'tema': tema, 'video': video, 'descripcion_video': descripcion_video,
               'es_favorito': es_favorito, 'origen_no_youtube': origen_no_youtube,
               'num_respuestas_video': num_respuestas_video,
               'posts': posts, 'populares': populares, 'propio_video': propio_video,
               'recientes': recientes, 'cita': cita, 'form_respuesta': form_respuesta,
               'hora_procesada_video': hora_procesada_video}

    return render(request, template, context)


@login_required
def sumar_post_video(request, slug, video_id):
    # procesa un nuevo post en el video.
    tema = get_object_or_404(Temas, slug=slug)
    video_padre = get_object_or_404(Videos, id=video_id)
    if request.method == "POST":
        form = FormNuevoPost(request.POST)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            post_video = Posts(texto=texto, creador=perfil_usuario,
                               tema=tema, video=video_padre)
            post_video.save()

            # Notificacion respuesta
            if perfil_usuario != video_padre.perfil:
                notificacion_respuesta = Notificacion(actor=perfil_usuario, target=video_padre.perfil,
                                                      objeto_id=video_padre.id, tipo_objeto="video",
                                                      tipo_notificacion="comment")
                notificacion_respuesta.save()

            # calcular nivel actividad y de popularidad del Tema
            popularidad_actividad_tema(tema, "positivo")

            return HttpResponseRedirect(reverse('videos:video',
                                                kwargs={'video_id': video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))
        else:
            pass
    else:
        return HttpResponseRedirect(reverse('videos:video',
                                            kwargs={'video_id': video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))


@login_required
def marcar_favorito(request):
    # Marca un video como favorito del usuario
    if request.is_ajax():
        video_id = request.GET.get('video_id', '')
        video = get_object_or_404(Videos, id=video_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        # reveisa si ya marco como favorito ese video
        fue_eliminado = False
        registro_existe = VFavoritos.objects.filter(
            video=video, perfil=perfil_usuario).exists()
        if registro_existe:
            registro_favorito = VFavoritos.objects.get(
                video=video, perfil=perfil_usuario)
            fue_eliminado = registro_favorito.eliminado
            if fue_eliminado:
                video.favoritos_recibidos += 1
                registro_favorito.eliminado = False
                video.save()
                registro_favorito.save()
                return HttpResponse("favorito marcado")

            else:
                # le esta eliminando de sus favoritos
                video.favoritos_recibidos -= 1
                registro_favorito.eliminado = True
                video.save()
                registro_favorito.save()
                return HttpResponse("favorito eliminado")
        else:
            # Crea un nuevo registro de video favorito
            video.favoritos_recibidos += 1
            registro_favorito = VFavoritos(video=video, perfil=perfil_usuario)
            video.save()
            registro_favorito.save()

            # calcular nivel actividad y de popularidad del Tema
            popularidad_actividad_tema(video.tema, "positivo")

            #Notificaciones video
            if perfil_usuario != video.perfil:
                notificacion_video_fav = Notificacion(actor=perfil_usuario, target=video.perfil,
                                                      objeto_id=video.id, tipo_objeto="video",
                                                      tipo_notificacion="fav_voteup")
                notificacion_video_fav.save()

            # Notificación por num de favoritos
            if video.favoritos_recibidos == 100 or video.favoritos_recibidos == 1000:
                notificacion_video_num = Notificacion(target=video.perfil,
                                                      objeto_id=video.id, tipo_objeto="video",
                                                      tipo_notificacion="num")
                notificacion_video_num.save()

        return HttpResponse("nuevo favorito marcado")
    else:
        raise Http404


@login_required
def denunciar_video(request):
    if request.is_ajax():
        reputacion_necesaria = 10
        video_id = request.GET.get('video_id')
        video = get_object_or_404(Videos, id=video_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

        ya_denuncio = False
        ya_denuncio = VDenunciados.objects.filter(
            video=video, perfil=perfil_usuario).exists()
        if ya_denuncio:
            return HttpResponse('video ya denunciado')
        else:
            if perfil_usuario.votos_recibidos >= reputacion_necesaria:
                vdenunciado_object = VDenunciados(
                    video=video, perfil=perfil_usuario)
                video.denunciado += 1
                vdenunciado_object.save()
                video.save()
                # Los videos denunciados no son eliminados automáticamente, son revisados primero.

            return HttpResponse('video denunciado')


def post_video(request, video_id, slug, post_id, queryset):
    # Pagina que muestra un post con el video donde fue posteado y sus respuestas.
    template = 'videos/post_video.html'
    perfil_usuario = None
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # Video
    video = get_object_or_404(Videos, id=video_id)
    es_favorito = "no_es_favorito"
    propio_video = False
    if request.user.is_authenticated():
        if video.perfil == perfil_usuario:  # El usuario visitante subió el video
            propio_video = True
        if VFavoritos.objects.filter(video=video, perfil=perfil_usuario, eliminado=False).exists():
            es_favorito = "es_favorito"  # El video es favorito del usuario visitante
    num_respuestas_video = Posts.objects.filter(
        video=video, eliminado=False).count()
    descripcion_video = procesar_espacios(video.descripcion)
    hora_procesada_video = tiempo_desde(video.fecha)

    # Tema
    tema_obj = get_object_or_404(Temas, slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (
            Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
        descripcion_tema = procesar_espacios(descripcion_tema)
    else:
        descripcion_tema = "No tiene descripción por el momento"
    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

    # Post
    post_obj = get_object_or_404(Posts, id=post_id)
    post = obtener_args_post(post_obj, perfil_usuario)

    # post_padre
    post_padre = []
    if post_obj.es_respuesta is True:
        # respuestas post_padre_object.
        respuesta_obj = Respuestas.objects.get(post_respuesta=post_obj)
        post_padre_obj = respuesta_obj.post_padre
        post_padre = obtener_args_post(post_padre_obj, perfil_usuario)

    # respuestas al post con respecto al queryset
    recientes = ""
    primeras = ""
    if queryset == "primeras":
        q = 'id'
        primeras = "subrayar"
    else:
        q = '-id'
        recientes = "subrayar"

    respuestas_obj = Respuestas.objects.filter(
        post_padre=post_obj).order_by(q)
    respuestas = []
    for r in respuestas_obj:
        post_respuesta = r.post_respuesta
        if post_respuesta.eliminado is False:
            respuesta = obtener_args_post(post_respuesta, perfil_usuario)
            respuestas_respuesta = obtener_respuestas_post(post_respuesta)
            respuesta.append(respuestas_respuesta)
            respuestas.append(respuesta)

    # form_respuestas, mismo que para todos los posts
    form_respuesta = FormNuevoPost()

    context = {'tema': tema, 'video': video, 'descripcion_video': descripcion_video,
               'es_favorito': es_favorito, 'post': post, 'post_padre': post_padre,
               'respuestas': respuestas, 'num_respuestas_video': num_respuestas_video,
               'post': post, 'primeras': primeras, 'recientes': recientes,
               'form_respuesta': form_respuesta, 'propio_video': propio_video,
               'hora_procesada_video': hora_procesada_video}

    return render(request, template, context)
