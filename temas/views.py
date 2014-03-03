# -*- coding: utf-8 -*-
from datetime import datetime
import random
import re

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import User

from forms import FormCrearTema, FormNuevoPost
from models import *
from perfiles.models import Perfiles
from citas.models import Cita
from imagenes.models import Imagen

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
	query_string = ""
	found_entries = None
	if ('q' in request.GET) and request.GET['q'].strip():
		query_string = request.GET['q']
		entry_query = get_query(query_string, ['nombre',])
		found_entries = Temas.objects.filter(entry_query).order_by('-nivel_popularidad')
		context = {'query_string':query_string, 'found_entries':found_entries}
		return render(request, 'temas/busqueda.html', context)

def main(request):
	#muestra la pagina principal de todos los temas
	temas = Temas.objects.all().order_by('nombre')
	indexes = range(7)
	random.shuffle(indexes)
	posts_populares = []
	for i in range(3):
		pp = Posts.objects.filter(es_respuesta=False).order_by('-votos_positivos')[indexes.pop()]
		posts_populares.append(pp)

	z = 0
	if len(temas) < 20:
		z = len(temas)
	else:
		z = 15

	temas_populares = Temas.objects.order_by('-nivel_popularidad')[:z]
	temas_activos = Temas.objects.order_by('-nivel_actividad')[:z]

	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	context = {'temas': temas, 'posts_populares': posts_populares,
	'temas_populares':temas_populares, 'temas_activos': temas_activos,
	'cita':cita}
	return render(request, 'temas/main.html', context)

def nuevo_tema(request):
	if request.method == "POST":
		form = FormCrearTema(request.POST)
		if form.is_valid():
			nuevo_tema = form.save(commit=False)
			perfil_usuario = Perfiles.objects.get(usuario = request.user)
			nuevo_tema.creador = perfil_usuario
			nuevo_tema.save()

			return HttpResponseRedirect(reverse('temas:main'))
		else:
			pass #!!! enviar errores

	form_crear_tema = FormCrearTema()
	context = {'form_crear_tema':form_crear_tema}
	return render(request, 'temas/nuevo_tema.html', context)

def index_tema(request, titulo):
	#muestra la pagina principal del tema
	tema = Temas.objects.get(nombre=titulo)
	posts_tema = Posts.objects.filter(tema = tema, es_respuesta = False).order_by('-id')
	
	imagenes_objects = Imagen.objects.all().order_by('-favoritos_recibidos')[:5]
	imagenes_display = []
	primera_imagen = ""
	primero = True
	for i in imagenes_objects:
		if primero == True:
			primera_imagen = i.url
			primero = False
		else:
			imagenes_display.append(i.url)

	context = {'tema':tema, 'posts_tema':posts_tema, 
	'imagenes_display': imagenes_display,
	'primera_imagen':primera_imagen}
	return render(request, 'temas/tema.html', context)


def sumar_post(request, tema):
	if request.method == "POST":
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			tema_contenedor = Temas.objects.get(nombre = tema)
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

			return HttpResponseRedirect(reverse('temas:index_tema', args = (tema,)))
		else:
			pass #!!! enviar errores

	return HttpResponseRedirect(reverse('temas:nuevo_post', args = (tema,)))

def nuevo_post(request, tema):
	form_nuevo_post = FormNuevoPost()
	tema_contenedor = Temas.objects.get(nombre = tema)
	context = {'form_nuevo_post': form_nuevo_post, 'tema':tema_contenedor}
	return render(request, 'temas/nuevo_post.html', context)

def post(request, tema, post_id):
	form_respuesta = FormNuevoPost() #utiliza el mismo form que los posts normales
	post = Posts.objects.get(id=post_id)
	res_crudo = Respuestas.objects.filter(post_padre = post).order_by('-id')
	#obtiene los objetos de la tabla respuestas para trabajar con ellos.
	respuestas = []
	#lista en la que se van a guardar los objetos de la tabla Posts correspondientes.
	for r in res_crudo:
		respuestas.append(r.post_respuesta)
	tema = Temas.objects.get(nombre=tema)

	suma_votos = post.votos_positivos - post.votos_negativos
	context = {'tema': tema, 'post':post, 'form_respuesta': form_respuesta, 
	'respuestas':respuestas, 'suma_votos':suma_votos}
	return render(request, 'temas/post.html', context)

def respuesta(request, tema, post_id):
	if request.method == "POST":
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			tema_contenedor = Temas.objects.get(nombre = tema)
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
			args =(tema.nombre, post_id)))

def voto(request, post_id, tema):
	if request.method == "POST":
		voto = request.POST.get("voto")
		if voto == "positivo":
			#si la funcion recibe en el Post el string "positivo".
			#encuentra el Post object, el Perfil del votante y del votado.
			#revisa si ya voto el usuario en ese post. Boolean, variable "ya_voto".
			post_votado = Posts.objects.get(id=post_id)
			autor_post = post_votado.creador
			usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
			usuario_votante = Perfiles.objects.get(usuario = request.user)
			ya_voto = Votos.objects.filter(post_votado = post_votado, 
				usuario_votante = usuario_votante).exists()
			
			if ya_voto:
				#si ya voto, obtiene el objecto Voto que esta guardado en la bd.
				voto_actual = Votos.objects.get(post_votado = post_votado, 
				usuario_votante = usuario_votante)
				if voto_actual.tipo == 1:
					#si el voto actual es positivo recarga la pagina.
					#no se puede votar 2 veces positivo.
					#pasa el string tema que recibe la funcion como argumento.
					return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))
				elif voto_actual.tipo == -1:
					#si el voto actual es negativo cambia el voto a positivo
					voto_actual.tipo = 1
					voto_actual.save()
					#resta 1 a los negativos y suma 1 a los positivos del objeto Post
					#el objeto Post lleva cuenta aparte para simplificar querys
					post_votado.votos_negativos -= 1
					post_votado.votos_positivos += 1
					post_votado.save()

					#suma a la cantidad de votos positivos que ha recibido el usuario.
					usuario_votado.votos_recibidos += 1
					usuario_votado.save()

					return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))
			else:
				#Si no existe un voto del usuario en ese post
				#crea un voto Positivo de ese usario en ese post.
				voto = Votos(usuario_votado=usuario_votado,
					usuario_votante=usuario_votante,
					post_votado = post_votado, tema = post_votado.tema, tipo = 1)
				#1 positivo. -1 negativo
				voto.save()

				#suma 1 a los votos_positivos del objeto usuario
				post_votado.votos_positivos += 1
				post_votado.save()

				#suma 1 a los votos recibidos del usuario_votado.
				usuario_votado.votos_recibidos += 1
				usuario_votado.save()

				return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))
	
		elif voto == "negativo":
			#los mismo que con los votos positivos con una diferencia:
			#no resta votos_recibidos al usuario_votado si el voto es nuevo.
			#asi, se evita usuarios con puntaje negativo.
			post_votado = Posts.objects.get(id=post_id)
			autor_post = post_votado.creador
			usuario_votado = Perfiles.objects.get(usuario=autor_post.usuario)
			usuario_votante = Perfiles.objects.get(usuario = request.user)
			ya_voto = Votos.objects.filter(post_votado = post_votado, 
				usuario_votante = usuario_votante).exists()
			if ya_voto:
				voto_actual = Votos.objects.get(post_votado = post_votado, 
				usuario_votante = usuario_votante)
				if voto_actual.tipo == -1:
					return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))
				elif voto_actual.tipo == 1:
					voto_actual.tipo = -1
					voto_actual.save()

					post_votado.votos_negativos += 1
					post_votado.votos_positivos -= 1
					post_votado.save()

					usuario_votado.votos_recibidos -= 1
					usuario_votado.save()

					return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))
			else:
				voto = Votos(usuario_votado=usuario_votado,
					usuario_votante=usuario_votante,
					post_votado = post_votado, tema = post_votado.tema, tipo = -1)
				#1 positivo. -1 negativo
				voto.save()

				post_votado.votos_negativos += 1
				post_votado.save()
			
				return HttpResponseRedirect(reverse('temas:index_tema', 
					args =(tema,)))

		else:
			pass #!!! 404
	else:
		pass #!!! 404 request no es post




