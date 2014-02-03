# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from forms import FormCrearTema, FormNuevoPost
from django.core.urlresolvers import reverse
from models import Temas, Posts
from perfiles.models import Perfiles
from django.contrib.auth.models import User

def main(request):
	#muestra la pagina principal de todos los temas
	temas = Temas.objects.all()
	context = {'temas': temas}
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
	posts_tema = Posts.objects.filter(tema = tema).order_by('-id')
	context = {'tema':tema, 'posts_tema':posts_tema}
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
	context = {'tema': tema, 'post':post, 'form_respuesta': form_respuesta}
	return render(request, 'temas/post.html', context)

def respuesta(request, tema, post_id):
	if request.method == "POST":
		form = FormNuevoPost(request.POST)
		if form.is_valid():
			texto = form.cleaned_data.get('texto')
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			tema_contenedor = Temas.objects.get(nombre = tema)
			post_padre = Posts.objects.get(id=post_id)
			post_respuesta = Post(texto=texto, es_respuesta = True, creador = perfil_usuario,
				tema = tema_contenedor)
			respuesta_db = Respuestas(post_respuesta=post_respuesta, post_padre = post_padre)
			post_respuesta.save()
			respuesta_db.save()
			return HttpResponseRedirect(reverse('temas:post', args =(tema_contenedor.nombre, post_padre.id)))
		else:
			pass #!!! enviar errores
	else:
		tema = Temas.objects.get(nombre = tema)

		return HttpResponseRedirect(reverse('temas:post', args =(tema.nombre, post_id)))
