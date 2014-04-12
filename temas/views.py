# -*- coding: utf-8 -*-
from datetime import datetime
import random
import re
import json

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from endless_pagination.decorators import page_template
from django.views.decorators.csrf import ensure_csrf_cookie
from forms import FormCrearTema, FormNuevoPost, FormEditarTema
from models import *
from perfiles.models import Perfiles
from citas.models import Cita
from imagenes.models import Imagen
from utils import obtener_posts_populares, obtener_imagen

#print "variable %s" %(variable) <--- para debug
@ensure_csrf_cookie
def prueba(request):
	template = "temas/prueba.html"
	print "llego def prueba"

	data = {}
	context = {}
	return render(request, template, context)

def prueba_ajax(request):
	print "llego a def prueba_ajax"
	if request.is_ajax():
		print "request is ajax!"
		variable = request.GET.get('data', '')
		print variable
		data = {}
		data['variable']='se recibio la data y esta es la respuesta :)'
		return HttpResponse(json.dumps(data), content_type = "application/json")
	else:
		return HttpResponse('no_ajax')

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

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
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
		entry_query = get_query(query_string, ['nombre',])
		found_entries = Temas.objects.filter(entry_query).order_by('-nivel_popularidad')
		context = {'query_string':query_string, 'found_entries':found_entries}
		return render(request, template, context)

@page_template('index_page_temas.html')
def main(request, queryset, template = 'temas/main.html', extra_context = None):
	#muestra la pagina principal de todos los temas
	posts_populares = obtener_posts_populares()

	todos = ""
	activos = ""
	populares = ""
	q = ""
	if queryset == "populares":
		q = "-nivel_popularidad"
		populares = "active"
	elif queryset == "todos" :
		q = "nombre"
		todos = "active"
	else:
		q = "-nivel_actividad"
		activos = "active"

	temas = []
	temas_obj = Temas.objects.order_by(q)
	for tema in temas_obj:
		if Tema_descripcion.objects.filter(tema=tema).exists():
			descripcion_obj = Tema_descripcion.objects.filter(tema=tema).latest('id')
			descripcion = descripcion_obj.texto
		else:
			descripcion = ""
		imagen = obtener_imagen(tema.id)
		temas.append([tema, descripcion, imagen])

	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	imagenes_posts_populares = []
	for post in posts_populares:
		imagen = obtener_imagen(post.tema.id)
		imagenes_posts_populares.append(imagen)

	context = {'temas': temas, 'posts_populares': posts_populares,
	'cita':cita, 'todos':todos, 'activos':activos, 'populares':populares,
	'imagenes_posts_populares':imagenes_posts_populares}

	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

def nuevo_tema(request):
	template = 'temas/nuevo_tema.html'

	if request.method == "POST":
		form = FormCrearTema(request.POST)
		if form.is_valid():
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			nombre = form.cleaned_data.get('nombre')
			texto = form.cleaned_data.get('texto')
			imagen = form.cleaned_data.get('imagen')
			tema_obj = Temas(nombre=nombre, creador=perfil_usuario, imagen = imagen)
			tema_obj.save()

			tema_descripcion_obj = Tema_descripcion(texto=texto, usuario=perfil_usuario,
				tema=tema_obj)

			tema_descripcion_obj.save()

			return HttpResponseRedirect(reverse('temas:main', kwargs={'queryset':(u'recientes')}))
		else:
			pass #!!! enviar errores

	form_crear_tema = FormCrearTema()
	context = {'form_crear_tema':form_crear_tema}
	return render(request, template, context)

@page_template('index_page_posts.html')
def index_tema(request, slug , queryset, template = 'temas/tema.html', extra_context = None):
	#muestra la pagina principal del tema
	
	#Tema object.
	tema = Temas.objects.get(slug=slug)
	descripcion = ""
	if Tema_descripcion.objects.filter(tema=tema).exists():
		descripcion_obj = Tema_descripcion.objects.filter(tema=tema).latest('id')
		descripcion = descripcion_obj.texto
	imagen = obtener_imagen(tema.id)

	#Posts
	populares = ""
	recientes = ""
	if queryset == "populares":
		q = "-votos_positivos"
		populares = "active"
	else:
		q = "-id"
		recientes = "active"
	posts_obj = Posts.objects.filter(tema = tema, eliminado=False, es_respuesta=False).order_by(q)
	posts = []
	for post in posts_obj:
		#lista de posts con respuestas y con voted status incluido
		num_respuestas = Respuestas.objects.filter(post_padre=post).count()
		voted_status = "no-vote"
		if post.creador.usuario == request.user:
			voted_status = "propio_post"
			print "propio post"
		else:
			if Votos.objects.filter(post_votado=post, usuario_votante=request.user).exists():
				voto = Votos.objects.get(post_votado=post, usuario_votante=request.user)
				if voto.tipo == 1:
					voted_status = "voted-up"
				elif voto.tipo == -1:
					voted_status = "voted-down"
				else:
					voted_status = "no-vote"

		puntaje = post.votos_positivos-post.votos_negativos

		posts.append([post,num_respuestas, voted_status, puntaje])

	# thumbnail de imágenes.
	imagenes_ids = [44,47,38,41,35,42]
	random.shuffle(imagenes_ids)
	imagenes_display = []

	for x in imagenes_ids:
		img = Imagen.objects.get(id=x)
		imagenes_display.append(img.url)


	context = {'tema':tema, 'imagen': imagen, 'posts':posts,'descripcion':descripcion,
	'imagenes_display': imagenes_display, 'recientes':recientes, 'populares':populares,
	}

	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

def sumar_post(request, slug):
	template = 'temas/nuevo_post.html'
	if request.method == "POST":
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			tema_contenedor = Temas.objects.get(slug = slug)
			post = Posts(texto = texto, creador = perfil_usuario, tema = tema_contenedor)
			post.save()
			#sumar a nivel de popularidad del Tema
			tema_contenedor.nivel_popularidad += 1
			#calcular nivel actividad del Tema
			cinco_posts = Posts.objects.filter(tema=tema_contenedor).order_by('-fecha')[:5]
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
			tema_contenedor.nivel_actividad = n_actividad

			tema_contenedor.save()

			return HttpResponseRedirect(reverse('temas:index_tema', 
				kwargs = {'slug':tema_contenedor.slug, 'queryset': u'recientes'}))
		else:
			pass #!!! enviar errores

	form_nuevo_post = FormNuevoPost()
	tema_contenedor = Temas.objects.get(slug = slug)

	context = {'form_nuevo_post': form_nuevo_post, 'tema':tema_contenedor}
	return render(request, template, context)

def post(request, slug, post_id):
	template = 'temas/post.html'

	#post_padre
	post_padre = Posts.objects.get(id=post_id)
	post_es_respuesta = False
	suma_votos = post_padre.votos_positivos - post_padre.votos_negativos

	post_padre_padre = ""
	post_pp_respuestas = 0
	if post_padre.es_respuesta == True:
		post_es_respuesta = True
		#respuestas_post_padre_object. El post padre del post si el post es respuesta.
		rpp_obj = Respuestas.objects.get(post_respuesta=post_padre)
		post_padre_padre = rpp_obj.post_padre
		post_pp_respuestas = Respuestas.objects.filter(post_padre=post_padre_padre).count()

	#respuestas
	respuestas_obj = Respuestas.objects.filter(post_padre = post_padre).order_by('-id')
	print "respuestas_obj: %s" %(respuestas_obj)
	respuestas = []
	#obtiene los objetos de la tabla respuestas para trabajar con ellos.
	#lista en la que se van a guardar los objetos de la tabla Posts correspondientes.
	for r in respuestas_obj:
		post_obj = r.post_respuesta
		print "post_obj.id: %s" %(post_obj.id)
		num_respuestas_respuesta = Respuestas.objects.filter(post_padre=post_obj).count()
		respuestas.append([r.post_respuesta, num_respuestas_respuesta])
		print "num_respuestas_respuesta: %s" %(num_respuestas_respuesta)
	#tema
	tema = Temas.objects.get(slug=slug)
	imagen_tema = obtener_imagen(tema.id)
	descripcion_tema = Tema_descripcion.objects.filter(tema=tema).latest('id')
	posts_count = Posts.objects.filter(tema=tema, eliminado=False, es_respuesta=False).count()

	#otros
	form_respuesta = FormNuevoPost() #utiliza el mismo form que los posts normales
	
	context = {'tema': tema, 'imagen_tema':imagen_tema, 'post_es_respuesta':post_es_respuesta,
	'post_padre':post_padre, 'form_respuesta': form_respuesta, 
	'respuestas':respuestas, 'suma_votos':suma_votos,
	'descripcion_tema':descripcion_tema, 'posts_count':posts_count,
	'post_es_respuesta':post_es_respuesta, 'post_padre_padre':post_padre_padre,
	'post_pp_respuestas':post_pp_respuestas}

	return render(request, template, context)

def respuesta(request, slug, post_id):
	if request.method == "POST":
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			tema_contenedor = Temas.objects.get(slug=slug)
			post_padre = Posts.objects.get(id=post_id)
			post_respuesta = Posts(texto=texto, es_respuesta = True,
				creador = perfil_usuario,
				tema = tema_contenedor)
			post_respuesta.save()

			respuesta_db = Respuestas(post_respuesta=post_respuesta,
				post_padre = post_padre)
			respuesta_db.save()
			
			return HttpResponseRedirect(reverse('temas:post', 
				args =(tema_contenedor.nombre, post_padre.id)))
		else:
			pass #!!! enviar errores
	else:
		tema = Temas.objects.get(nombre = tema)

		return HttpResponseRedirect(reverse('temas:post', 
			kwargs = {'slug': tema.slug, 'post_id': post_id}))

def remover_voto_ajax(request):
	if request.is_ajax():
		post_id = request.GET.get('post_id','')
		post_votado = Posts.objects.get(id=post_id)
		autor_post = post_votado.creador
		usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
		usuario_votante = Perfiles.objects.get(usuario = request.user)
		voto_actual = Votos.objects.get(post_votado = post_votado, 
			usuario_votante = usuario_votante)
		if voto_actual.tipo == 1:
			post_votado.votos_positivos -=1
			usuario_votado.votos_recibidos -= 1
		elif voto_actual.tipo == -1:
			post_votado.votos_positivos += 1
			usuario_votado.votos_recibidos += 1

		voto_actual.tipo = 0
		post_votado.save()
		usuario_votado.save()
		voto_actual.save()
		return HttpResponse('remover_voto_ajax hecho')
	else:
		return HttpResponse('error_no_ajax')

def vote_up_ajax(request):
	if request.is_ajax():
		print "voted-up"
		post_id = request.GET.get('post_id','')
		#encuentra el Post object, el Perfil del votante y del votado.
		#revisa si ya voto el usuario en ese post. Boolean, variable "ya_voto".
		post_votado = Posts.objects.get(id=post_id)
		print "post_id %s" %(post_id)
		print "post_votado.votos_positivos %s" %(post_votado.votos_positivos)
		print "post_votado.votos_negativos %s" %(post_votado.votos_negativos)
		autor_post = post_votado.creador
		usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
		usuario_votante = Perfiles.objects.get(usuario = request.user)

		if usuario_votado == usuario_votante:
			return HttpResponse('no puedes votar tus propios post')
		else:
			ya_voto = Votos.objects.filter(post_votado = post_votado, 
				usuario_votante = usuario_votante).exists()
			if ya_voto:
				#si ya voto, obtiene el objecto Voto que esta guardado en la bd.
				voto_actual = Votos.objects.get(post_votado = post_votado, 
				usuario_votante = usuario_votante)
				print "ya voto"
				print "voto_actual.tipo %s" %(voto_actual.tipo)

				if voto_actual.tipo == -1:
					#si el voto actual es negativo cambia el voto a positivo
					voto_actual.tipo = 1
					voto_actual.save()
					#resta 1 a los negativos y suma 1 a los positivos del objeto Post
					#el objeto Post lleva cuenta aparte para simplificar querys
					post_votado.votos_negativos -= 1
					post_votado.votos_positivos += 1
					post_votado.save()

					print "post_votado.votos_positivos %s" %(post_votado.votos_positivos)
					print "post_votado.votos_negativos %s" %(post_votado.votos_negativos)
					print "total: %s" %(post_votado.votos_positivos-post_votado.votos_negativos)

					#suma a la cantidad de votos positivos que ha recibido el usuario.
					usuario_votado.votos_recibidos += 1
					usuario_votado.save()

				elif voto_actual.tipo == 0:
					voto_actual.tipo = 1
					post_votado.votos_positivos += 1
					usuario_votado.votos_recibidos += 1
					voto_actual.save()
					post_votado.save()
					usuario_votado.save()
			else:
				"nuevo voto creado"
				#Si no existe un voto del usuario en ese post
				#crea un voto Positivo de ese usario en ese post.
				voto = Votos(usuario_votado=usuario_votado,
					usuario_votante=usuario_votante,
					post_votado = post_votado, tema = post_votado.tema, tipo = 1)
				#1 positivo. -1 negativo
				voto.save()

				#suma 1 a los votos_positivos del objeto post
				post_votado.votos_positivos += 1
				post_votado.save()

				#suma 1 a los votos recibidos del usuario_votado.
				usuario_votado.votos_recibidos += 1
				usuario_votado.save()

			return HttpResponse('vote-up ajax procesado')
	else:
		return HttpResponse('error_no_ajax')

def vote_down_ajax(request):
	if request.is_ajax():
		post_id = request.GET.get('post_id','')
		#los mismo que con los votos positivos con una diferencia:
		#no resta votos_recibidos al usuario_votado si el voto es nuevo.
		#asi, se evita usuarios con puntaje negativo.
		post_votado = Posts.objects.get(id=post_id)

		autor_post = post_votado.creador
		usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
		usuario_votante = Perfiles.objects.get(usuario = request.user)

		if usuario_votado == usuario_votante:
			return HttpResponse('no puedes votar tus propios post')
		else:
			ya_voto = Votos.objects.filter(post_votado = post_votado, 
				usuario_votante = usuario_votante).exists()
			if ya_voto:
				voto_actual = Votos.objects.get(post_votado = post_votado, 
				usuario_votante = usuario_votante)

				if voto_actual.tipo == 1:
					voto_actual.tipo = -1
					voto_actual.save()

					post_votado.votos_negativos += 1
					post_votado.votos_positivos -= 1
					post_votado.save()

					usuario_votado.votos_recibidos -= 1
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
					post_votado = post_votado, tema = post_votado.tema, tipo = -1)
				voto.save()

				post_votado.votos_negativos += 1
				post_votado.save()
			
			return HttpResponse('vote-down ajax procesado')
	else:
		return HttpResponse('error_no_ajax')

def editar_tema(request, slug):
	template = "temas/editar_tema.html"

	tema = Temas.objects.get(slug=slug)
	perfil_usuario = Perfiles.objects.get(usuario=request.user)
	reputacion_necesaria = 10
	if request.method == "POST":
		form = FormEditarTema(request.POST)
		if form.is_valid():
			descripcion = form.cleaned_data['descripcion']
			if len(descripcion)>30:
				tema_descripcion_obj = Tema_descripcion(texto=descripcion,
				usuario=perfil_usuario, tema=tema)
				tema_descripcion_obj.save()
			imagen = form.cleaned_data['imagen']
			if len(imagen)>10:
				tema.imagen = imagen
				tema.save()
		else:
			pass
			#!!! enviar errores
		return HttpResponseRedirect(reverse('temas:index_tema', 
						kwargs={'slug':slug, 'queryset':u'recientes'}))
	
	puede_editar = True
	if perfil_usuario.votos_recibidos < reputacion_necesaria:
		puede_editar = False

	ha_sido_editado = False
	tiene_descripcion = False
	primera_edicion, ultima_edicion = "",""
	numero_de_ediciones = 0

	if Tema_descripcion.objects.filter(tema=tema).exists():
		tiene_descripcion = True
		ediciones = Tema_descripcion.objects.filter(tema=tema).order_by('id')
		numero_de_ediciones = ediciones.count()
		primera_edicion_obj = ediciones[0]
		primera_edicion = primera_edicion_obj.texto
		if numero_de_ediciones > 1:
			ha_sido_editado = True
			ultima_edicion_obj = ediciones.reverse()[0]
			ultima_edicion = ultima_edicion_obj.texto
		else:
			ultima_edicion = primera_edicion

	imagen = obtener_imagen(tema.id)

	if primera_edicion == "":
		primera_edicion = "Este tema no tiene descripción, todavía."
		tiene_descripcion = False
	print primera_edicion

	form_editar_tema = FormEditarTema(initial={'descripcion':ultima_edicion})
	

	context = {'puede_editar':puede_editar, 'primera_edicion':primera_edicion,
	'ultima_edicion':ultima_edicion, 'numero_de_ediciones':numero_de_ediciones,
	'tema':tema, 'form_editar_tema':form_editar_tema,
	'ha_sido_editado':ha_sido_editado, 'imagen':imagen,
	'tiene_descripcion':tiene_descripcion}

	return render(request, template, context)

def eliminar_propio_post(request, post_id):
	post = Posts.objects.get(id=post_id)
	if post.creador.usuario == request.user:
		post.eliminado = True
		post.save()
		return redirect('temas:main', queryset = u'recientes' )
	else:
		return redirect('temas:main', queryset = u'recientes' )