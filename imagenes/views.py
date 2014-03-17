# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum


from models import Imagen, Ifavoritas, Idenunciadas
from forms import FormNuevaImagen
from perfiles.models import Perfiles
from citas.models import Cita

def index(request):
	imagenes_fecha = Imagen.objects.filter(eliminada=False).order_by('-fecha')

	context = {'imagenes_fecha':imagenes_fecha}
	return render(request, 'imagenes/index.html', context)

def populares(request):
	imagenes_populares = Imagen.objects.filter(eliminada=False).order_by('-favoritos_recibidos')

	context = {'imagenes_populares':imagenes_populares}
	return render(request, 'imagenes/populares.html', context)

def nueva(request):
	if request.method == "POST":
		form = FormNuevaImagen(request.POST)
		if form.is_valid():
			favorita = form.cleaned_data['favorita']
			url = form.cleaned_data['url']
			print "url: %s" %(url)
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			nueva_imagen = Imagen(url=url, perfil=perfil_usuario)
			nueva_imagen.save()
			if favorita:
				nueva_imagen.favoritos_recibidos += 1
				Ifavorita_obj = Ifavoritas(imagen=nueva_imagen, perfil=perfil_usuario)
				Ifavorita_obj.save()
				nueva_imagen.save()

			return HttpResponseRedirect(reverse('imagenes:index'))
		else:
			pass #!!! enviar errores
	else:
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
	print "propio_usuario: %s" %(propio_usuario)
	cita = Cita.objects.filter(favoritos_recibidos__gt=1).latest('fecha')

	context = {'imagenes_favoritas':imagenes_favoritas, 'usuario_fav':usuario_fav,
	'propio_usuario':propio_usuario, 'cita':cita, 'username':username}
	return render(request, 'imagenes/favoritas.html', context)

def denunciar(request, imagen_id):
	imagen = Imagen.objects.get(pk=imagen_id)
	perfil_usuario = Perfiles.objects.get(usuario=request.user)

	#ya_denuncio = Idenunciadas.objects.filter(imagen=imagen, perfil=perfil_usuario)
	ya_denuncio = False
	if ya_denuncio:
		print "ya denuncio"
		print imagen.denunciada
		return redirect('imagenes:index')
	else:
		idenunciada_object = Idenunciadas(imagen=imagen, perfil=perfil_usuario)
		imagen.denunciada += 1
		print imagen.denunciada
		idenunciada_object.save()
		if imagen.denunciada > 3:
			imagen.eliminada = True
		imagen.save()
	return redirect('imagenes:index')

def colaborar_organizar(request):
	progress_bar = 100
	imagenes_denunciadas = []
	hay_imagenes_denunciadas = Imagen.objects.filter(eliminada=True, removidatotalmente=False).exists()
	if hay_imagenes_denunciadas:
		imagenes_denunciadas_obj = Imagen.objects.filter(eliminada=True, removidatotalmente=False)
		success_uno = "#dff0d8"
		success_dos = "#d0e9c6"
		danger_uno = "#f2dede"
		danger_dos = "#ebcccc"
		default = "#ebebeb"
		
		vistos_totales = imagenes_denunciadas_obj.aggregate(Sum('vistos_recibidos'))
		x_totales = imagenes_denunciadas_obj.aggregate(Sum('xrecibidas'))
		suma_x_vistos = vistos_totales['vistos_recibidos__sum'] + x_totales['xrecibidas__sum']
		max_posible = imagenes_denunciadas_obj.count()*3
		porcentaje_avanzado = (float(suma_x_vistos)/float(max_posible))*100
		progress_bar = str(porcentaje_avanzado)

		for i in imagenes_denunciadas_obj:
			x = []
			estado = []
			color = ""
			puntos = i.vistos_recibidos - i.xrecibidas
			if puntos < 0:
				if puntos < -1:
					color = danger_dos
					estado = ["remove", "remove"]
				else:
					color = danger_uno
					estado = ["remove"]
			elif puntos > 0:
				if puntos > 1:
					color = success_dos
					estado = ["ok", "ok"]
				else:
					color = success_uno
					estado = ["ok"]
			else:
				color = default

			print "estado : %s" %(estado)

			x.append([i.id,i.url,i.favoritos_recibidos,color, estado])
			imagenes_denunciadas.append(x)

	context = {'imagenes_denunciadas':imagenes_denunciadas, 'progress_bar':progress_bar,
	'hay_imagenes_denunciadas':hay_imagenes_denunciadas}
	return render(request, 'imagenes/imagenes_coorg.html', context)

def marcar_visto(request, imagen_id):
	#!!! falta limitar a un visto por usuario con una nueva tabla
	imagen = Imagen.objects.get(id=imagen_id)
	if imagen.xrecibidas > 0:
		imagen.xrecibidas -= 1
	else:
		imagen.vistos_recibidos += 1
		if imagen.vistos_recibidos >= 3:
			imagen.eliminada = False
			imagen.vistos_recibidos = 0
			imagen.denunciada = 0
	imagen.save()
	return redirect('imagenes:colaborar_organizar')

def marcar_x(request, imagen_id):
	#!!! falta limitar a una x por usuario con una nueva tabla
	imagen = Imagen.objects.get(id=imagen_id)
	if imagen.vistos_recibidos > 0:
		print "aca"
		imagen.vistos_recibidos -= 1
	else:
		imagen.xrecibidas += 1
		if imagen.xrecibidas >= 3:
			imagen.removidatotalmente = True
			imagen.xrecibidas = 0
			imagen.denunciada = 0
	imagen.save()
	return redirect('imagenes:colaborar_organizar')
