# -*- coding: utf-8 -*-
# VIEW.PY VIDEO

import urlparse
from datetime import datetime

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from endless_pagination.decorators import page_template

from perfiles.models import Perfiles
from forms import FormNuevoVideo
from temas.forms import FormNuevoPost
from models import Videos, VFavoritos, VDenunciados
from temas.models import Temas, Tema_descripcion, Posts, Respuestas
from citas.models import Cita
from olibertaria.utils import obtener_imagen_tema, obtener_voted_status

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
			nuevo_video = Videos(tema = tema, perfil = perfil_usuario, titulo = titulo, \
				descripcion=descripcion, url = url, es_youtube=es_youtube, youtube_id=youtube_id)
			nuevo_video.save()
			return redirect('temas:index_tema', slug=tema.slug, queryset='recientes')
		else:
			return redirect('videos:nuevo_video', slug=tema.slug)
			#!!! enviar errores
	else:
		form_nuevo_video = FormNuevoVideo()
		context = {'form_nuevo_video':form_nuevo_video, 'tema':tema}
		return render(request, template, context)

@page_template('index_page_videos.html')
def videos_tema(request, slug, queryset, template = 'videos/videos_tema.html', extra_context=None):
	#La pagina principal del tema pero desplegando los videos.
	perfil_usuario = Perfiles.objects.get(usuario=request.user)

	#Tema
	tema_obj = Temas.objects.get(slug=slug)
	imagen_tema = obtener_imagen_tema(tema_obj)
	if Tema_descripcion.objects.filter(tema=tema_obj).exists():
		descripcion_tema = (Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
	else:
		descripcion_tema = "No tiene descripción por el momento"
	posts_count = Posts.objects.filter(tema=tema_obj, eliminado=False, es_respuesta=False).count()
	tema = [tema_obj, imagen_tema, descripcion_tema, posts_count]

	#Videos
	populares = ""
	recientes = ""
	if queryset == "populares":
		q = "-favoritos_recibidos"
		populares = "active"
	else:
		q = '-id'
		recientes = "active"

	videos = []
	videos_obj = Videos.objects.filter(tema=tema_obj, eliminado=False).order_by(q)
	videos_favoritos_obj = VFavoritos.objects.filter(perfil=perfil_usuario, eliminado=False)
	videos_favoritos_ids = []
	for v in videos_favoritos_obj:
		videos_favoritos_ids.append(int(v.video.id))

	for video in videos_obj:
		if video.es_youtube == True:
			imagen_video = "http://img.youtube.com/vi/%s/0.jpg" %(video.youtube_id)
		else:
			imagen_video = "http://www.flaticon.es/png/256/24933.png"
		
		es_favorito = "no_es_favorito"
		if video.id in videos_favoritos_ids:
			es_favorito= "es_favorito"

		videos.append([video, imagen_video, es_favorito])
		
		print es_favorito

	#cita
	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	context = {'tema':tema, 'populares':populares, 'recientes':recientes, 
	'videos':videos, 'cita':cita}

	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

def video(request, video_id, slug, queryset):
	template = 'videos/video.html'
	perfil_usuario = Perfiles.objects.get(usuario=request.user)

	#Video
	video = Videos.objects.get(id=video_id)
	es_favorito = "no_es_favorito"
	if VFavoritos.objects.filter(video=video, perfil=perfil_usuario, eliminado=False).exists():
		es_favorito = "es_favorito"
	num_respuestas_video = Posts.objects.filter(video=video, eliminado=False).count()
	
	#Tema
	tema_obj = Temas.objects.get(slug=slug)
	imagen_tema = obtener_imagen_tema(tema_obj)
	if Tema_descripcion.objects.filter(tema=tema_obj).exists():
		descripcion_tema = (Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
	else:
		descripcion_tema = "No tiene descripción por el momento"
	posts_count = Posts.objects.filter(tema=tema_obj, eliminado=False, es_respuesta=False).count()
	video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
	tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

	#Posts de respuesta al video
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
		#Respuestas y voted status
		num_respuestas = Respuestas.objects.filter(post_padre = post, post_respuesta__eliminado=False).count()
		voted_status = obtener_voted_status(post, perfil_usuario)
		posts.append([post, num_respuestas, voted_status])

	#cita
	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	#form_respuesta
	form_respuesta = FormNuevoPost()

	context = {'tema':tema, 'video':video, 'es_favorito':es_favorito, 
	'num_respuestas_video':num_respuestas_video, 'posts':posts, 'populares':populares,
	'recientes':recientes, 'cita':cita, 'form_respuesta':form_respuesta}

	return render(request, template, context)

def sumar_post_video(request, slug, video_id):
	tema = Temas.objects.get(slug = slug)
	video_padre = Videos.objects.get(id=video_id)
	if request.method == "POST":
		print "llego respuesta con post"
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			print "form is valid respuesta"
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			post_video = Posts(texto=texto, creador = perfil_usuario,tema = tema, video=video_padre)
			post_video.save()

			#sumar a nivel de popularidad del Tema
			tema.nivel_popularidad += 1
			#calcular nivel actividad del Tema
			cinco_posts = Posts.objects.filter(tema=tema).order_by('-fecha')[:5]
			n_actividad = 0
			hoy = datetime.today()
			for post in cinco_posts:
				f = post.fecha
				if hoy.month == f.month:
					if hoy.day - f.day < 7:
						n_actividad += 5
					elif hoy.day - f.day <15:
						n_actividad += 3
					else:
						n_actividad += 1
			tema.nivel_actividad = n_actividad

			tema.save()

			print "respuesta guardada"			
			return HttpResponseRedirect(reverse('videos:video', 
				kwargs = {'video_id':video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))
		else:
			print "form invalid"
			pass #!!! enviar errores
	else:
		print "llego respuesta sin post"
		return HttpResponseRedirect(reverse('videos:video', 
				kwargs = {'video_id':video_padre.id, 'slug': tema.slug, 'queryset': u'recientes'}))

def marcar_favorito(request):
	if request.is_ajax():
		video_id = request.GET.get('video_id', '')
		print video_id
		video = Videos.objects.get(id=video_id)
		perfil_usuario = Perfiles.objects.get(usuario=request.user)
		#reveisa si ya marco como favorito ese video
		fue_eliminado = False
		registro_existe = VFavoritos.objects.filter(video=video, perfil=perfil_usuario).exists()
		if registro_existe:
			registro_favorito = VFavoritos.objects.get(video=video, perfil=perfil_usuario)
			fue_eliminado = registro_favorito.eliminado
			if fue_eliminado:
				video.favoritos_recibidos +=1
				registro_favorito.eliminado = False
				video.save()
				registro_favorito.save()
				return HttpResponse("favorito marcado")

			else:
				#le esta eliminando de sus favoritos
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
		return HttpResponse("nuevo favorito massrcado")
	#!!! falta 404 si la respuesta no es ajax.

def denunciar(request):
	if request.is_ajax():
		video_id = request.GET.get('video_id')
		video = Videos.objects.get(id=video_id)
		perfil_usuario = Perfiles.objects.get(usuario=request.user)

		ya_denuncio=False
		ya_denuncio = VDenunciados.objects.filter(video=video, perfil=perfil_usuario).exists()
		if ya_denuncio:
			return HttpResponse('video ya denunciado')
		else:
			if perfil_usuario.votos_recibidos > 10:
				vdenunciada_object = VDenunciados(video=video, perfil=perfil_usuario)
				video.denunciado += 1
				vdenunciada_object.save()
				if video.denunciado > 3:
					video.eliminado = True
				video.save()
			return HttpResponse('video denunciado')

def post_video(request, video_id, slug, post_id, queryset):
	template = 'videos/post_video.html'
	perfil_usuario = Perfiles.objects.get(usuario=request.user)

	#Video
	video = Videos.objects.get(id=video_id)
	es_favorito = "no_es_favorito"
	if VFavoritos.objects.filter(video=video, perfil=perfil_usuario, eliminado=False).exists():
		es_favorito = "es_favorito"
	num_respuestas_video = Posts.objects.filter(video=video, eliminado=False).count()
	
	#Tema
	tema_obj = Temas.objects.get(slug=slug)
	imagen_tema = obtener_imagen_tema(tema_obj)
	if Tema_descripcion.objects.filter(tema=tema_obj).exists():
		descripcion_tema = (Tema_descripcion.objects.filter(tema=tema_obj).latest('id')).texto
	else:
		descripcion_tema = "No tiene descripción por el momento"
	posts_count = Posts.objects.filter(tema=tema_obj, eliminado=False, es_respuesta=False).count()
	video_count = Videos.objects.filter(tema=tema_obj, eliminado=False).count()
	tema = [tema_obj, imagen_tema, descripcion_tema, posts_count, video_count]

	#Post
	post_obj = Posts.objects.get(id=post_id)
	post_voted_status = obtener_voted_status(post_obj, perfil_usuario)
	post_numrespuestas = Respuestas.objects.filter(post_padre=post_obj, post_respuesta__eliminado=False).count()
	post=[post_obj, post_voted_status, post_numrespuestas]

	#post_padre
	post_padre = []
	if post_obj.es_respuesta == True:
		#respuestas post_padre_object. El post padre del post si el post es respuesta.
		respuesta_obj = Respuestas.objects.get(post_respuesta=post_obj)
		post_padre_obj = respuesta_obj.post_padre
		post_padre_estado = obtener_voted_status(post_padre_obj, perfil_usuario)
		post_padre_numrespuestas = Respuestas.objects.filter(post_padre=post_padre_obj, post_respuesta__eliminado=False).count()
		post_padre = [post_padre_obj, post_padre_estado, post_padre_numrespuestas]

	#respuestas
	recientes = ""
	primeras = ""
	if queryset == "primeras":
		q = 'id'
		primeras = "subrayar"
	else:
		q = '-id'
		recientes = "subrayar"

	respuestas_obj = Respuestas.objects.filter(post_padre = post_obj).order_by(q)
	respuestas = []
	#lista en la que se van a guardar los objetos de la tabla Posts correspondientes.
	for r in respuestas_obj:
		post_respuesta = r.post_respuesta
		if post_respuesta.eliminado == False:
			respuesta_numrespuestas = Respuestas.objects.filter(post_padre=post_respuesta, post_respuesta__eliminado=False).count()
			respuesta_estado = obtener_voted_status(post_respuesta, perfil_usuario)
			respuestas.append([post_respuesta, respuesta_numrespuestas, respuesta_estado])

	#cita
	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	#form_respuestas
	form_respuesta = FormNuevoPost()

	context = {'tema':tema, 'video':video, 'es_favorito':es_favorito, 
	'post':post, 'post_padre':post_padre, 'respuestas':respuestas,
	'num_respuestas_video':num_respuestas_video, 'post':post, 'primeras':primeras,
	'recientes':recientes, 'cita':cita, 'form_respuesta':form_respuesta}

	return render(request, template, context)
