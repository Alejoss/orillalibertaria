# -*- coding: utf-8 -*-
# VIEW.PY VIDEO

import urlparse
from datetime import datetime

from django.http import Http404
from django.shortcuts import render, redirect
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
from olibertaria.utils import obtener_imagen_tema, obtener_voted_status


@login_required
def nuevo_video(request, slug):
    template = 'videos/nuevo.html'
    tema = Temas.objects.get(slug=slug)
    if request.method == 'POST':
        form = FormNuevoVideo(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            url_data = urlparse.urlparse(url)
            query = urlparse.parse_qs(url_data.query)
            network_location = url_data.netloc
            youtube_id = ""
            if network_location in ("www.youtube.com", "youtube.com"):
                es_youtube = True
                youtube_id = query['v'][0]
            else:
                es_youtube = False
            nuevo_video = Videos(
                tema=tema, perfil=perfil_usuario, titulo=titulo,
                descripcion=descripcion, url=url, es_youtube=es_youtube, youtube_id=youtube_id)
            nuevo_video.save()
            return redirect('videos:videos_tema', slug=tema.slug, queryset='recientes')
        else:
            return redirect('videos:nuevo_video', slug=tema.slug)
    else:
        form_nuevo_video = FormNuevoVideo()
        context = {'form_nuevo_video': form_nuevo_video, 'tema': tema}
        return render(request, template, context)


@login_required
def editar_video(request, video_id):
    template = 'videos/editar_video.html'
    video = Videos.objects.get(id=video_id)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    if video.perfil == perfil_usuario:
        if request.method == "POST":
            form = FormEditarVideo(request.POST)
            if form.is_valid():
                url = form.cleaned_data['url']
                titulo = form.cleaned_data['titulo']
                descripcion = form.cleaned_data['descripcion']
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
            form_editar_video = FormEditarVideo(initial={'url': video.url, 'titulo': video.titulo,
                                                         'descripcion': video.descripcion})
            context = {'video': video, 'form_editar_video': form_editar_video}
            return render(request, template, context)
    else:
        raise Http404


@page_template('index_page_videos.html')
def videos_tema(request, slug, queryset, template='videos/videos_tema.html', extra_context=None):
    # La pagina principal del tema pero desplegando los videos.
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # Tema
    tema_obj = Temas.objects.get(slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (
            Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
    else:
        descripcion_tema = "No tiene descripción por el momento"
    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count]

    # Videos
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
        if request.user.is_authenticated():
            if video.id in videos_favoritos_ids:
                es_favorito = "es_favorito"

        num_respuestas_video = Posts.objects.filter(
            video=video, eliminado=False).count()

        videos.append([video, imagen_video, es_favorito, num_respuestas_video])

    # cita
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    context = {'tema': tema, 'populares': populares, 'recientes': recientes,
               'videos': videos, 'cita': cita}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@page_template('index_page_videos_favoritos.html')
def videos_perfil(request, username, template="videos/videos_perfil.html", extra_context=None):
    # View para la pagina de videos del usuario
    user_object = User.objects.get(username=username)
    perfil_usuario = Perfiles.objects.get(usuario=user_object)
    propio_usuario = False
    if request.user.is_authenticated():
        perfil_usuario_visitante = Perfiles.objects.get(usuario=request.user)
        if perfil_usuario == perfil_usuario_visitante:
            propio_usuario = True
        else:
            propio_usuario = False

    # Videos
    videos_favoritos_obj = VFavoritos.objects.filter(
        perfil=perfil_usuario, eliminado=False)
    videos_obj = []
    for v in videos_favoritos_obj:
        videos_obj.append(v.video)
    videos = []

    if request.user.is_authenticated():
        for video in videos_obj:
            if propio_usuario:
                es_favorito = "es_favorito"
            else:
                if VFavoritos.objects.filter(video=video, perfil=perfil_usuario_visitante, eliminado=False).exists():
                    es_favorito = "es_favorito"
                else:
                    es_favorito = "no_es_favorito"
    else:
        es_favorito = "no_es_favorito"

    for video in videos_obj:
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
               'propio_usuario': propio_usuario, 'cita': cita}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


def video(request, video_id, slug, queryset):
    template = 'videos/video.html'
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

    num_respuestas_video = Posts.objects.filter(
        video=video, eliminado=False).count()
    origen_no_youtube = ""
    if video.es_youtube is False:
        if "vimeo.com" in video.url:
            origen_no_youtube = "vimeo"
        elif "ted.com" in video.url:
            origen_no_youtube = "ted"

    # Tema
    tema_obj = Temas.objects.get(slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (
            Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
    else:
        descripcion_tema = "No tiene descripción por el momento"
    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

    # Posts de respuesta al video
    populares = ""
    recientes = ""
    if queryset == "populares":
        q = "-votos_total"
        populares = "subrayar"
    else:
        q = "-id"
        recientes = "subrayar"

    posts_obj = Posts.objects.filter(video=video, eliminado=False).order_by(q)
    posts = []
    for post in posts_obj:
        # Respuestas y voted status
        num_respuestas = Respuestas.objects.filter(
            post_padre=post, post_respuesta__eliminado=False).count()
        if request.user.is_authenticated():
            voted_status = obtener_voted_status(post, perfil_usuario)
        else:
            voted_status = "no-vote"
        posts.append([post, num_respuestas, voted_status])

    # cita
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    # form_respuesta
    form_respuesta = FormNuevoPost()

    context = {'tema': tema, 'video': video, 'es_favorito': es_favorito,
               'origen_no_youtube': origen_no_youtube, 'num_respuestas_video': num_respuestas_video,
               'posts': posts, 'populares': populares, 'propio_video': propio_video,
               'recientes': recientes, 'cita': cita, 'form_respuesta': form_respuesta}

    return render(request, template, context)


@login_required
def sumar_post_video(request, slug, video_id):
    tema = Temas.objects.get(slug=slug)
    video_padre = Videos.objects.get(id=video_id)
    if request.method == "POST":
        form = FormNuevoPost(request.POST)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            post_video = Posts(texto=texto, creador=perfil_usuario,
                               tema=tema, video=video_padre)
            post_video.save()

            #Notificacion respuesta
            notificacion_respuesta = Notificacion(actor=perfil_usuario, target=video_padre.creador,
                                                  objeto_id=video_padre.id, tipo_objeto="video",
                                                  tipo_notificacion="comment")
            notificacion_respuesta.save()

            # sumar a nivel de popularidad del Tema
            tema.nivel_popularidad += 1
            # calcular nivel actividad del Tema
            cinco_posts = Posts.objects.filter(
                tema=tema).order_by('-fecha')[:5]
            n_actividad = 0
            hoy = datetime.today()
            for post in cinco_posts:
                f = post.fecha
                if hoy.month == f.month:
                    if hoy.day - f.day < 7:
                        n_actividad += 5
                    elif hoy.day - f.day < 15:
                        n_actividad += 3
                    else:
                        n_actividad += 1
            tema.nivel_actividad = n_actividad

            tema.save()

            return HttpResponseRedirect(reverse('videos:video',
                                                kwargs={'video_id': video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))
        else:
            pass  # !!! enviar errores
    else:
        return HttpResponseRedirect(reverse('videos:video',
                                            kwargs={'video_id': video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))


@login_required
def marcar_favorito(request):
    if request.is_ajax():
        video_id = request.GET.get('video_id', '')
        video = Videos.objects.get(id=video_id)
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
            video.favoritos_recibidos += 1
            registro_favorito = VFavoritos(video=video, perfil=perfil_usuario)
            video.save()
            registro_favorito.save()

            #Notificaciones video
            if perfil_usuario != video.perfil:
                notificacion_video_fav = Notificacion(actor=perfil_usuario, target=video.perfil,
                                                      objeto_id=video.id, tipo_objeto="video",
                                                      tipo_notificacion="fav_voteup")
                notificacion_video_fav.save()

            if video.favoritos_recibidos == 100 or video.favoritos_recibidos == 1000:
                notificacion_video_num = Notificacion(target=video.perfil,
                                                      objeto_id=video.id, tipo_objeto="video",
                                                      tipo_notificacion="num")
                notificacion_video_num.save()

        return HttpResponse("nuevo favorito marcado")
    #!!! falta 404 si la respuesta no es ajax.


@login_required
def denunciar_video(request):
    if request.is_ajax():
        video_id = request.GET.get('video_id')
        video = Videos.objects.get(id=video_id)
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

        ya_denuncio = False
        ya_denuncio = VDenunciados.objects.filter(
            video=video, perfil=perfil_usuario).exists()
        if ya_denuncio:
            return HttpResponse('video ya denunciado')
        else:
            if perfil_usuario.votos_recibidos > 10:
                vdenunciado_object = VDenunciados(
                    video=video, perfil=perfil_usuario)
                video.denunciado += 1
                vdenunciado_object.save()
                video.save()

            return HttpResponse('video denunciado')


def post_video(request, video_id, slug, post_id, queryset):
    template = 'videos/post_video.html'
    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # Video
    video = Videos.objects.get(id=video_id)
    es_favorito = "no_es_favorito"
    if request.user.is_authenticated():
        if VFavoritos.objects.filter(video=video, perfil=perfil_usuario, eliminado=False).exists():
            es_favorito = "es_favorito"
    num_respuestas_video = Posts.objects.filter(
        video=video, eliminado=False).count()

    # Tema
    tema_obj = Temas.objects.get(slug=slug)
    imagen_tema = obtener_imagen_tema(tema_obj)
    if Tema_descripcion.objects.filter(tema=tema_obj).exists():
        descripcion_tema = (
            Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
    else:
        descripcion_tema = "No tiene descripción por el momento"
    posts_count = Posts.objects.filter(
        tema=tema_obj, eliminado=False, es_respuesta=False).count()
    video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

    # Post
    post_obj = Posts.objects.get(id=post_id)
    if request.user.is_authenticated():
        post_voted_status = obtener_voted_status(post_obj, perfil_usuario)
    else:
        post_voted_status = "no-vote"
    post_numrespuestas = Respuestas.objects.filter(
        post_padre=post_obj, post_respuesta__eliminado=False).count()
    post = [post_obj, post_voted_status, post_numrespuestas]

    # post_padre
    post_padre = []
    if post_obj.es_respuesta is True:
        # respuestas post_padre_object. El post padre del post si el post es
        # respuesta.
        respuesta_obj = Respuestas.objects.get(post_respuesta=post_obj)
        post_padre_obj = respuesta_obj.post_padre
        if request.user.is_authenticated():
            post_padre_estado = obtener_voted_status(post_padre_obj, perfil_usuario)
        else:
            post_padre_estado = "no-vote"
        post_padre_numrespuestas = Respuestas.objects.filter(
            post_padre=post_padre_obj, post_respuesta__eliminado=False).count()
        post_padre = [post_padre_obj,
                      post_padre_estado, post_padre_numrespuestas]

    # respuestas
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
    # lista en la que se van a guardar los objetos de la tabla Posts
    # correspondientes.
    for r in respuestas_obj:
        post_respuesta = r.post_respuesta
        if post_respuesta.eliminado is False:
            respuesta_numrespuestas = Respuestas.objects.filter(
                post_padre=post_respuesta, post_respuesta__eliminado=False).count()
            if request.user.is_authenticated():
                respuesta_estado = obtener_voted_status(post_respuesta, perfil_usuario)
            else:
                respuesta_estado = "no-vote"
            respuestas.append(
                [post_respuesta, respuesta_numrespuestas, respuesta_estado])

    # cita
    cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

    # form_respuestas
    form_respuesta = FormNuevoPost()

    context = {'tema': tema, 'video': video, 'es_favorito': es_favorito,
               'post': post, 'post_padre': post_padre, 'respuestas': respuestas,
               'num_respuestas_video': num_respuestas_video, 'post': post, 'primeras': primeras,
               'recientes': recientes, 'cita': cita, 'form_respuesta': form_respuesta}

    return render(request, template, context)

