# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from models import Imagen, Ifavoritas
from forms import FormNuevaImagen
from perfiles.models import Perfiles
from citas.models import Cita

def index(request):
	imagenes_fecha = Imagen.objects.filter(eliminada=False).order_by('-fecha')
	imagenes_populares = Imagen.objects.filter(eliminada=False).order_by('-votos_recibidos')
	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	context = {'imagenes_fecha':imagenes_fecha, 'imagenes_populares':imagenes_populares,
	'cita':cita}
	return render(request, 'imagenes/index.html', context)

def nueva(request):
	if request.method == "POST":
		print 1
		form = FormNuevaImagen(request.POST)
		if form.is_valid():
			print 2
			nueva_imagen = form.save(commit=False)
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			nueva_imagen.perfil = perfil_usuario
			nueva_imagen.save()
			print 3
			return HttpResponseRedirect(reverse('imagenes:index'))
		else:
			pass #!!! enviar errores
	else:
		print 5
		form = FormNuevaImagen()
		context = {'FormNuevaImagen':FormNuevaImagen}
		return render(request, 'imagenes/nueva.html', context)

def marcar_favorito(request, imagen_id):
	imagen = Imagen.objects.get(pk=imagen_id)
	perfil_usuario = Perfiles.objects.get(usuario=request.user)
	#revisa si ya marco como favorito a esa imagen
	fue_eliminado = False
	registro_existe = Ifavoritas.objects.filter(imagen=imagen, perfil = perfil_usuario).exists()
	if registro_existe:
		print 1
		registro_favorito = Ifavoritas.objects.get(imagen=imagen, perfil = perfil_usuario)
		fue_eliminado = registro_favorito.eliminado
		if fue_eliminado == True:
			print 2
			imagen.favoritos_recibidos += 1
			registro_favorito.eliminado = False
			imagen.save()
			registro_favorito.save()
			return HttpResponseRedirect(reverse('imagenes:index'))
		else:
			print 3
			imagen.favoritos_recibidos -= 1
			registro_favorito.eliminado = True
			registro_favorito.portada = False #Asegurarse de que no van a haber 2 portadas.
			imagen.save()
			registro_favorito.save()
			return HttpResponseRedirect(reverse('imagenes:index'))
	else:
		print 4
		imagen.favoritos_recibidos += 1
		registro_favorito = Ifavoritas(imagen=imagen, perfil = perfil_usuario)
		registro_favorito.save()
		imagen.save()
		return HttpResponseRedirect(reverse('imagenes:index'))

def marcar_portada(request, imagen_id):
	imagen = Imagen.objects.get(pk=imagen_id)
	perfil_usuario = Perfiles.objects.get(usuario=request.user)
	
	ya_tiene_portada = Ifavoritas.objects.filter(perfil=perfil_usuario, eliminado=False, portada=True).exists()
	if ya_tiene_portada:
		portada_actual = Ifavoritas.objects.get(perfil=perfil_usuario, eliminado=False, portada=True)
		portada_actual.portada = False
		portada_actual.save()
		registro_portada = Ifavoritas.objects.get(imagen=imagen, perfil=perfil_usuario, eliminado=False)
		registro_portada.portada=True
		registro_portada.save()
	else:
		registro_portada = Ifavoritas.objects.get(imagen=imagen, perfil=perfil_usuario, eliminado=False)
		registro_portada.portada=True
		registro_portada.save()

	return redirect('imagenes:favoritas', username=request.user.username)

def favoritas(request, username):
	user_object = User.objects.get(username=username)
	perfil_usuario = Perfiles.objects.get(usuario=user_object)
	Ifavoritas_objects = Ifavoritas.objects.filter(perfil = perfil_usuario, eliminado=False).order_by('-fecha')
	imagenes_favoritas = []
	for c in Ifavoritas_objects:
		if c.portada == True:
			imagenes_favoritas.append([c.imagen, True])
		else:
			imagenes_favoritas.append([c.imagen, False])
	usuario_fav = user_object.username

	propio_usuario = False
	if request.user == user_object:
		propio_usuario = True

	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	context = {'imagenes_favoritas':imagenes_favoritas, 'usuario_fav':usuario_fav,
	'propio_usuario':propio_usuario, 'cita':cita}
	return render(request, 'imagenes/favoritas.html', context)

def prueba(request):
	return render(request, 'imagenes/prueba.html')
