# -*- coding: utf-8 -*-
# VIEWS TEMAS

from datetime import datetime
import re
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from endless_pagination.decorators import page_template

from forms import FormCrearTema, FormNuevoPost, FormEditarTema, FormEditarPost
from models import Temas, Posts, Respuestas, Votos, Tema_descripcion
from notificaciones.models import Notificacion
from perfiles.models import Perfiles
from citas.models import Cita
from videos.models import Videos
from imagenes.models import Imagen
from olibertaria.utils import obtener_imagenes_display, obtener_voted_status,\
    obtener_imagen_tema, obtener_cita, procesar_espacios, bersuit_vergarabat, tiempo_desde,\
    obtener_respuestas_post
from utils import obtener_posts_populares, obtener_videos_populares

# print "variable %s" %(variable) <--- para debug


def inicio(request):
    template = 'inicio.html'
    flecha_hidden = "hidden"  # navbar link a Inicio.

    # objetivos, para el progress bar.
    objetivo_temas = 100
    objetivo_posts = 500
    objetivo_videos = 500
    objetivo_imagenes = 500
    objetivo_frases = 500

    temas_actuales = Temas.objects.all().count()
    posts_actuales = Posts.objects.filter(eliminado=False, es_respuesta=False).count()
    videos_actuales = Videos.objects.filter(eliminado=False).count()
    imagenes_actuales = Imagen.objects.filter(eliminada=False).count()
    frases_actuales = Cita.objects.filter(eliminada=False).count()

    objetivos = {'objetivo_temas': objetivo_temas, 'objetivo_posts': objetivo_posts,
                 'objetivo_videos': objetivo_videos, 'objetivo_imagenes': objetivo_imagenes,
                 'objetivo_frases': objetivo_frases}

    actuales = {'temas_actuales': temas_actuales, 'posts_actuales': posts_actuales,
                'videos_actuales': videos_actuales, 'imagenes_actuales': imagenes_actuales,
                'frases_actuales': frases_actuales}

    # Progress bar, calcular porcentaje.
    temas_faltantes = objetivo_temas - temas_actuales

    if temas_faltantes < 0:
        temas_faltantes = 0
    porcentaje_temas = 1-(float(temas_faltantes)/float(objetivo_temas))

    posts_faltantes = objetivo_posts - posts_actuales
    if posts_faltantes < 0:
        posts_faltantes = 0
    porcentaje_posts = 1-(float(posts_faltantes)/float(objetivo_posts))

    videos_faltantes = objetivo_videos - videos_actuales
    if videos_faltantes < 0:
        videos_faltantes = 0
    porcentaje_videos = 1-(float(videos_faltantes)/float(objetivo_videos))

    imagenes_faltantes = objetivo_imagenes - imagenes_actuales
    if imagenes_faltantes < 0:
        imagenes_faltantes = 0
    porcentaje_imagenes = 1-(float(imagenes_faltantes)/float(objetivo_imagenes))

    frases_faltantes = objetivo_frases - frases_actuales
    if frases_faltantes < 0:
        frases_faltantes = 0
    porcentaje_frases = 1-(float(frases_faltantes)/float(objetivo_frases))

    progress_bar = (porcentaje_temas + porcentaje_posts +
                    porcentaje_videos + porcentaje_imagenes +
                    porcentaje_frases)/5
    progress_bar = str(progress_bar*100)

    context = {'flecha_hidden': flecha_hidden, 'progress_bar': progress_bar,
               'objetivos': objetivos, 'actuales': actuales}

    return render(request, template, context)


# Para el search de temas
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


# Para el search de temas
def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


def buscar(request):
    template = 'temas/busqueda.html'

    query_string = ""
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['nombre', ])
        found_entries = Temas.objects.filter(
            entry_query).order_by('-nivel_popularidad')
        temas_encontrados = []

        for tema in found_entries:
            if Tema_descripcion.objects.filter(tema=tema).exists():
                descripcion_obj = Tema_descripcion.objects.filter(
                    tema=tema).latest('id')
                descripcion = descripcion_obj.texto
            else:
                descripcion = ""

            imagen_tema = obtener_imagen_tema(tema)
            num_posts = Posts.objects.filter(tema=tema).count()
            num_videos = Videos.objects.filter(tema=tema).count()
            temas_encontrados.append(
                [tema, imagen_tema, descripcion, num_posts, num_videos])

        context = {'query_string': query_string,
                   'temas_encontrados': temas_encontrados}
        return render(request, template, context)
    else:
        return redirect('temas:main', queryset=u'activos')


@page_template('index_page_temas.html')
def main(request, queryset, template='temas/main.html', extra_context=None):
    # muestra la pagina principal de todos los temas
    # Post Popular
    post_popular = (obtener_posts_populares(1))[0]
    imagen_post_popular = obtener_imagen_tema(post_popular.tema)
    comments_post_popular = Respuestas.objects.filter(post_padre=post_popular).count()
    tema_posts_count = Posts.objects.filter(
        tema=post_popular.tema, eliminado=False, es_respuesta=False).count()
    tema_videos_count = Videos.objects.filter(
        tema=post_popular.tema, eliminado=False).count()

    # autocomplete search temas
    lista_temas_autocomplete = []
    for tema in Temas.objects.all():
        lista_temas_autocomplete.append(tema.nombre)
    lista_temas_json = json.dumps(lista_temas_autocomplete)

    # olibertaria datos
    num_temas_ol = Temas.objects.all().count()
    num_posts_ol = Posts.objects.filter(eliminado=False).count()
    num_videos_ol = Videos.objects.filter(eliminado=False).count()

    # Videos populares
    videos_populares_obj = obtener_videos_populares(3)
    videos_populares = []
    for video in videos_populares_obj:
        imagen_video = "http://img.youtube.com/vi/%s/0.jpg" % (video.youtube_id)
        videos_populares.append([video, imagen_video])

    # temas. ordenados por el queryset.
    recientes = ""
    activos = ""
    populares = ""
    q = ""
    if queryset == "populares":
        q = "-nivel_popularidad"
        populares = "active"
    elif queryset == "recientes":
        q = "-fecha_creacion"
        recientes = "active"
    else:
        q = "-nivel_actividad"
        activos = "active"

    temas = []
    temas_obj = Temas.objects.order_by(q)
    for tema in temas_obj:
        if Tema_descripcion.objects.filter(tema=tema).exists():
            descripcion_obj = Tema_descripcion.objects.filter(
                tema=tema).latest('id')
            descripcion = procesar_espacios(descripcion_obj.texto)
        else:
            descripcion = ""
        imagen = obtener_imagen_tema(tema)
        num_posts = Posts.objects.filter(tema=tema).count()
        num_videos = Videos.objects.filter(tema=tema).count()
        temas.append([tema, descripcion, imagen, num_posts, num_videos])

    # Cita sidebar
    cita_obj = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')
    cita = obtener_cita(cita_obj)

    context = {'temas': temas, 'post_popular': post_popular, 'videos_populares': videos_populares,
               'cita': cita, 'recientes': recientes, 'activos': activos,
               'populares': populares, 'imagen_post_popular': imagen_post_popular,
               'tema_posts_count': tema_posts_count,
               'tema_videos_count': tema_videos_count,
               'num_temas_ol': num_temas_ol, 'num_posts_ol': num_posts_ol,
               'num_videos_ol': num_videos_ol,
               'comments_post_popular': comments_post_popular,
               'lista_temas_json': lista_temas_json}

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@login_required
def nuevo_tema(request):
    template = 'temas/nuevo_tema.html'

    if request.method == "POST":
        form = FormCrearTema(request.POST)
        if form.is_valid():
            # Tema obj
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            nombre = form.cleaned_data.get('nombre')
            texto = form.cleaned_data.get('texto')
            imagen = form.cleaned_data.get('imagen')
            tema_obj = Temas(nombre=nombre,
                             creador=perfil_usuario, imagen=imagen)
            tema_obj.save()

            # Tema descripcion obj
            tema_descripcion_obj = Tema_descripcion(
                texto=texto, usuario=perfil_usuario,
                tema=tema_obj)

            tema_descripcion_obj.save()

            return HttpResponseRedirect(reverse('temas:main',
                                                kwargs={'queryset': (u'recientes')}))

    form_crear_tema = FormCrearTema()

    # honeypot
    lista_bersuit = bersuit_vergarabat()

    context = {'form_crear_tema': form_crear_tema, 'lista_bersuit': lista_bersuit}
    return render(request, template, context)


@page_template('index_page_posts.html')
def index_tema(request, slug, queryset, template='temas/tema.html', extra_context=None):
    # muestra la pagina principal del tema

    # Tema object.
    tema = get_object_or_404(Temas, slug=slug)
    descripcion = ""
    if Tema_descripcion.objects.filter(tema=tema).exists():
        descripcion_obj = Tema_descripcion.objects.filter(
            tema=tema).latest('id')
        descripcion = procesar_espacios(descripcion_obj.texto)
    imagen = obtener_imagen_tema(tema)

    # Posts
    populares = ""
    recientes = ""
    if queryset == "populares":
        q = "-votos_total"
        populares = "active"
    else:
        q = "-id"
        recientes = "active"
    posts_obj = Posts.objects.filter(
        tema=tema, eliminado=False, es_respuesta=False, video=None).order_by(q)
    posts = []
    for post in posts_obj:
        # lista de posts con respuestas y con voted status incluido
        num_respuestas = Respuestas.objects.filter(
            post_padre=post, post_respuesta__eliminado=False).count()
        if request.user.is_authenticated():
            perfil = Perfiles.objects.get(usuario=request.user)
            voted_status = obtener_voted_status(post, perfil)
        else:
            voted_status = "no-vote"

        texto_procesado = procesar_espacios(post.texto)
        respuestas = obtener_respuestas_post(post)  # respuestas vista previa
        hora_procesada = tiempo_desde(post.fecha)
        posts.append([post, num_respuestas, voted_status, texto_procesado,
                      hora_procesada, respuestas])

    # thumbnail de imágenes.
    imagenes_display = obtener_imagenes_display(7)

    context = {
        'tema': tema, 'imagen': imagen, 'posts': posts, 'descripcion': descripcion,
        'imagenes_display': imagenes_display, 'recientes': recientes, 'populares': populares,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render(request, template, context)


@login_required
def sumar_post(request, slug):
    template = 'temas/nuevo_post.html'
    if request.method == "POST":
        form = FormNuevoPost(request.POST)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            tema_contenedor = get_object_or_404(Temas, slug=slug)
            post = Posts(texto=texto, creador=perfil_usuario,
                         tema=tema_contenedor)
            post.save()

            # sumar a nivel de popularidad del Tema
            tema_contenedor.nivel_popularidad += 1

            # calcular nivel actividad del Tema
            cinco_posts = Posts.objects.filter(
                tema=tema_contenedor).order_by('-fecha')[:5]
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
            tema_contenedor.nivel_actividad = n_actividad
            tema_contenedor.save()

            return HttpResponseRedirect(reverse('temas:index_tema',
                                                kwargs={'slug': tema_contenedor.slug, 'queryset': u'recientes'}))

    form_nuevo_post = FormNuevoPost()
    tema_contenedor = get_object_or_404(Temas, slug=slug)

    context = {'form_nuevo_post': form_nuevo_post, 'tema': tema_contenedor}
    return render(request, template, context)


def post(request, slug, post_id, queryset):
    template = 'temas/post.html'

    if request.user.is_authenticated():
        perfil_usuario = Perfiles.objects.get(usuario=request.user)

    # tema
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
    videos_count = Videos.objects.filter(
        tema=tema_obj, eliminado=False).count()
    tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, videos_count]

    # post
    post_obj = get_object_or_404(Posts, id=post_id)
    if request.user.is_authenticated():
        post_voted_status = obtener_voted_status(post_obj, perfil_usuario)
    else:
        post_voted_status = "no-vote"
    post_numrespuestas = Respuestas.objects.filter(
        post_padre=post_obj, post_respuesta__eliminado=False).count()
    texto_procesado_post = procesar_espacios(post_obj.texto)
    hora_procesada = tiempo_desde(post_obj.fecha)
    post = [post_obj, post_voted_status, post_numrespuestas, texto_procesado_post, hora_procesada]

    # El post padre del post si el post es respuesta
    post_padre = []
    if post_obj.es_respuesta is True:
        # respuestas post_padre_object.
        respuesta_obj = Respuestas.objects.get(post_respuesta=post_obj)
        post_padre_obj = respuesta_obj.post_padre

        if request.user.is_authenticated():
            post_padre_estado = obtener_voted_status(post_padre_obj, perfil_usuario)
        else:
            post_padre_estado = "no-vote"

        post_padre_numrespuestas = Respuestas.objects.filter(
            post_padre=post_padre_obj, post_respuesta__eliminado=False).count()
        texto_procesado_postpadre = procesar_espacios(post_padre_obj.texto)
        hora_procesada = tiempo_desde(post_padre_obj.fecha)
        post_padre = [post_padre_obj, post_padre_estado, post_padre_numrespuestas,
                      texto_procesado_postpadre, hora_procesada]

    # respuestas Post, ordenadas por el queryset. suma la clase al filtro activo
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
            respuesta_numrespuestas = Respuestas.objects.filter(
                post_padre=post_respuesta, post_respuesta__eliminado=False).count()
            if request.user.is_authenticated():
                respuesta_estado = obtener_voted_status(post_respuesta, perfil_usuario)
            else:
                respuesta_estado = "no-vote"
            texto_procesado_resp = procesar_espacios(post_respuesta.texto)
            hora_procesada = tiempo_desde(post_respuesta.fecha)
            respuestas_respuesta = obtener_respuestas_post(post_respuesta)
            respuestas.append(
                [post_respuesta, respuesta_numrespuestas, respuesta_estado,
                 texto_procesado_resp, hora_procesada, respuestas_respuesta])

    # utiliza el mismo form que los posts normales
    form_respuesta = FormNuevoPost()

    context = {
        'tema': tema, 'descripcion_tema': descripcion_tema, 'posts_count': posts_count,
        'post': post, 'post_padre': post_padre, 'respuestas': respuestas,
        'form_respuesta': form_respuesta, 'recientes': recientes, 'primeras': primeras
    }

    return render(request, template, context)


@login_required
def editar_post(request, post_id):
    # Permite al usuario editar sus posts.
    post = get_object_or_404(Posts, id=post_id)
    if request.method == "POST":
        form = FormEditarPost(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            post.texto = texto
            post.save()
            return redirect('temas:post', slug=post.tema.slug, post_id=post.id, queryset=u'recientes')
        else:
            return redirect('temas:editar_post', post_id=post.id)
    else:
        template = 'temas/editar_post.html'
        perfil_usuario = Perfiles.objects.get(usuario=request.user)
        if perfil_usuario != post.creador:
            return redirect('temas:post', slug=post.tema.slug, post_id=post.id, queryset=u'recientes')
        else:
            form_editar_post = FormEditarPost(initial={'texto': post.texto})
            context = {'form_editar_post': form_editar_post, 'post': post}
            return render(request, template, context)


@login_required
def respuesta(request, slug, post_id):
    # Maneja la respuesta del usuario a un post. Cualquier post, sea respuesta o en video.
    tema = Temas.objects.get(slug=slug)
    if request.method == "POST":
        form = FormNuevoPost(request.POST)
        if form.is_valid():
            texto = form.cleaned_data.get('texto')
            perfil_usuario = Perfiles.objects.get(usuario=request.user)
            post_padre = Posts.objects.get(id=post_id)
            # Si es una respuesta a un post en un video
            if post_padre.video is not None:
                post_respuesta = Posts(texto=texto, es_respuesta=True,
                                       creador=perfil_usuario, tema=tema, video=post_padre.video)
            else:
                post_respuesta = Posts(texto=texto, es_respuesta=True,
                                       creador=perfil_usuario, tema=tema)

            post_respuesta.save()

            # Respuesta object
            respuesta_db = Respuestas(post_respuesta=post_respuesta,
                                      post_padre=post_padre)
            respuesta_db.save()

            #Notificacion respuesta
            if perfil_usuario != post_padre.creador:
                notificacion_respuesta = Notificacion(actor=perfil_usuario, target=post_padre.creador,
                                                      objeto_id=post_padre.id, tipo_objeto="post",
                                                      tipo_notificacion="comment")
                notificacion_respuesta.save()

            # Redirige a la pagina del post_video si pertenece a un video
            if post_padre.video is not None:
                return HttpResponseRedirect(reverse('videos:post_video',
                                                    kwargs={
                                                        'video_id': post_padre.video.id, 'slug': tema.slug,
                                                        'post_id': post_id,
                                                        'queryset': u'recientes'}))
            # Redirige a la pagina del post.
            else:
                return HttpResponseRedirect(reverse('temas:post',
                                                    kwargs={'slug': tema.slug, 'post_id': post_id,
                                                            'queryset': u'recientes'}))
    else:
        return HttpResponseRedirect(reverse('temas:post',
                                            kwargs={'slug': tema.slug, 'post_id': post_id,
                                                    'queryset': u'recientes'}))


@login_required
def remover_voto_ajax(request):
    # Quita el voto de un post que ya fue votado por el usuario.
    if request.is_ajax():
        post_id = request.GET.get('post_id', '')
        post_votado = get_object_or_404(Posts, id=post_id)
        autor_post = post_votado.creador
        usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
        usuario_votante = Perfiles.objects.get(usuario=request.user)
        voto_actual = Votos.objects.get(post_votado=post_votado,
                                        usuario_votante=usuario_votante)
        if voto_actual.tipo == 1:
            # Si es voto positivo, resta un voto.
            post_votado.votos_positivos -= 1
            usuario_votado.votos_recibidos -= 1
        elif voto_actual.tipo == -1:
            # Si es voto negativo, suma un voto.
            post_votado.votos_positivos += 1
            usuario_votado.votos_recibidos += 1

        voto_actual.tipo = 0  # Cambia el tipo de voto a neutral
        post_votado.save()
        usuario_votado.save()
        voto_actual.save()
        return HttpResponse('remover_voto_ajax')
    else:
        return HttpResponse('error_no_ajax')


@login_required
def vote_up_ajax(request):
    # Maneja con ajax el voto positivo de un usuario sobre un post.
    if request.is_ajax():
        post_id = request.GET.get('post_id', '')
        # encuentra el Post object, el Perfil del votante y del votado.
        # revisa si ya voto el usuario en ese post. Boolean, variable "ya_voto".
        post_votado = get_object_or_404(Posts, id=post_id)
        autor_post = post_votado.creador
        usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
        usuario_votante = Perfiles.objects.get(usuario=request.user)

        if usuario_votado == usuario_votante:
            return HttpResponse('no se puede votar en propios posts')
        else:
            ya_voto = Votos.objects.filter(post_votado=post_votado,
                                           usuario_votante=usuario_votante).exists()
            if ya_voto:
                # si ya voto, obtiene el objecto Voto.
                voto_actual = Votos.objects.get(post_votado=post_votado,
                                                usuario_votante=usuario_votante)

                if voto_actual.tipo == -1:
                    # si el voto actual es negativo cambia el voto a positivo
                    voto_actual.tipo = 1
                    voto_actual.save()
                    # resta 1 a los negativos y suma 1 a los positivos del objeto Post
                    # el objeto Post lleva cuenta aparte para simplificar
                    # querys
                    post_votado.votos_negativos -= 1
                    post_votado.votos_positivos += 1
                    post_votado.save()

                    # suma 2 a la cantidad de votos positivos que ha recibido el usuario.
                    usuario_votado.votos_recibidos += 2  # uno por borrar el negativo, otro por el positivo.
                    usuario_votado.save()

                elif voto_actual.tipo == 0:
                    voto_actual.tipo = 1
                    post_votado.votos_positivos += 1
                    usuario_votado.votos_recibidos += 1
                    voto_actual.save()
                    post_votado.save()
                    usuario_votado.save()
            else:
                # Si no existe un voto del usuario en ese post
                # crea un voto Positivo de ese usario en ese post.
                voto = Votos(usuario_votado=usuario_votado,
                             usuario_votante=usuario_votante,
                             post_votado=post_votado, tema=post_votado.tema, tipo=1)
                # 1 positivo. -1 negativo
                voto.save()

                # suma 1 a los votos_positivos del objeto post
                post_votado.votos_positivos += 1
                post_votado.save()

                # suma 1 a los votos recibidos del usuario_votado.
                usuario_votado.votos_recibidos += 1
                usuario_votado.save()

                # Notificacion post numero de votos altos
                if post_votado.votos_total == 100 or post_votado.votos_total == 1000:
                    notificacion_num = Notificacion(target=usuario_votado, objeto_id=post_votado.id,
                                                    tipo_objeto="post", tipo_notificacion="num")
                    notificacion_num.save()

                # Notificacion voteup
                if usuario_votante != usuario_votado:
                    notificacion_voteup = Notificacion(actor=usuario_votante, target=usuario_votado,
                                                       objeto_id=post_votado.id, tipo_objeto="post",
                                                       tipo_notificacion="fav_voteup")
                    notificacion_voteup.save()

            return HttpResponse('vote-up ajax procesado')
    else:
        return HttpResponse('error_no_ajax')


def vote_down_ajax(request):
    if request.is_ajax():
        # el save method del modelo se encarga de que el usuario no pueda tener puntaje negativo
        post_id = request.GET.get('post_id', '')
        post_votado = get_object_or_404(Posts, id=post_id)
        autor_post = post_votado.creador
        usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
        usuario_votante = Perfiles.objects.get(usuario=request.user)

        if usuario_votado == usuario_votante:
            return HttpResponse('no puedes votar tus propios post')
        else:
            ya_voto = Votos.objects.filter(post_votado=post_votado,
                                           usuario_votante=usuario_votante).exists()
            if ya_voto:
                voto_actual = Votos.objects.get(post_votado=post_votado,
                                                usuario_votante=usuario_votante)

                if voto_actual.tipo == 1:
                    voto_actual.tipo = -1
                    voto_actual.save()

                    post_votado.votos_negativos += 1
                    post_votado.votos_positivos -= 1
                    post_votado.save()

                    usuario_votado.votos_recibidos -= 2
                    usuario_votado.save()

                elif voto_actual.tipo == 0:
                    voto_actual.tipo = -1
                    post_votado.votos_negativos += 1
                    usuario_votado.votos_recibidos -= 1
                    voto_actual.save()
                    post_votado.save()
                    usuario_votado.save()
            else:
                voto = Votos(usuario_votado=usuario_votado,
                             usuario_votante=usuario_votante,
                             post_votado=post_votado, tema=post_votado.tema, tipo=-1)
                voto.save()

                usuario_votado.votos_recibidos -= 1
                post_votado.votos_negativos += 1
                usuario_votado.save()
                post_votado.save()

            return HttpResponse('vote-down ajax procesado')
    else:
        return HttpResponse('error_no_ajax')


@login_required
def editar_tema(request, slug):
    # Maneja el form y la pagina de editar tema
    template = "temas/editar_tema.html"

    tema = get_object_or_404(Temas, slug=slug)
    perfil_usuario = Perfiles.objects.get(usuario=request.user)
    reputacion_necesaria = 10

    if request.method == "POST":
        form = FormEditarTema(request.POST)
        if form.is_valid():
            descripcion = form.cleaned_data['descripcion']
            if len(descripcion) > 30:  # Jquery validate se asegura que la descripcion sea > 150 chars
                tema_descripcion_obj = Tema_descripcion(texto=descripcion,
                                                        usuario=perfil_usuario, tema=tema)
                tema_descripcion_obj.save()
            imagen = form.cleaned_data['imagen']
            if len(imagen) > 10:
                tema.imagen = imagen
                tema.save()

            return HttpResponseRedirect(reverse('temas:index_tema',
                                        kwargs={'slug': slug, 'queryset': u'recientes'}))
        else:
            pass

    puede_editar = True
    if perfil_usuario.votos_recibidos < reputacion_necesaria:
        puede_editar = False

    ha_sido_editado = False
    tiene_descripcion = False
    primera_edicion, ultima_edicion = "", ""
    numero_de_ediciones = 0

    if Tema_descripcion.objects.filter(tema=tema).exists():
        # Obtiene las ediciones al Tema
        tiene_descripcion = True
        ediciones = Tema_descripcion.objects.filter(tema=tema).order_by('id')
        numero_de_ediciones = ediciones.count()
        primera_edicion_obj = ediciones[0]  # Primera descripción del Tema
        primera_edicion = primera_edicion_obj.texto
        if numero_de_ediciones > 1:
            ha_sido_editado = True
            ultima_edicion_obj = ediciones.reverse()[0]  # Descripción actual del Tema
            ultima_edicion = ultima_edicion_obj.texto
        else:
            ultima_edicion = primera_edicion

    imagen = obtener_imagen_tema(tema)

    if primera_edicion == "":
        primera_edicion = "Este tema no tiene descripción, todavía."
        tiene_descripcion = False

    # llena el textarea de la descripción con la descripción actual
    form_editar_tema = FormEditarTema(initial={'descripcion': ultima_edicion})

    # Honeypot
    lista_bersuit = bersuit_vergarabat()

    context = {
        'puede_editar': puede_editar, 'primera_edicion': primera_edicion,
        'ultima_edicion': ultima_edicion, 'numero_de_ediciones': numero_de_ediciones,
        'tema': tema, 'form_editar_tema': form_editar_tema,
        'ha_sido_editado': ha_sido_editado, 'imagen': imagen,
        'tiene_descripcion': tiene_descripcion, 'lista_bersuit': lista_bersuit}

    return render(request, template, context)


@login_required
def eliminar_propio_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    if post.creador.usuario == request.user:
        # revisa que el usuario creador del post sea el mismo hecho login.
        if post.eliminado is False:
            post.eliminado = True
        elif post.eliminado is True:
            post.eliminado = False
        post.save()

    return redirect('temas:post', slug=post.tema.slug, post_id=post.id, queryset=u'recientes')
