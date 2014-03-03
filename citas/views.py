# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum

from models import Cita, Cfavoritas, Ceditadas
from perfiles.models import Perfiles
from forms import FormNuevaCita
from imagenes.models import Imagen

# Create your views here.
def index(request):
	citas_fecha = Cita.objects.filter(eliminada=False).order_by('-fecha')
	citas_por_autor = Cita.objects.filter(eliminada=False).order_by('autor')
	citas_populares = Cita.objects.filter(eliminada=False).order_by('-favoritos_recibidos')
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

	context = {'citas_fecha': citas_fecha, 'citas_por_autor':citas_por_autor, 
	'citas_populares':citas_populares, 'imagenes_display': imagenes_display,
	'primera_imagen':primera_imagen}
	return render(request, 'citas/index.html', context)

def nueva(request):
	if request.method == "POST":
		form = FormNuevaCita(request.POST)
		if form.is_valid():
			nueva_cita = form.save(commit=False)
			perfil_usuario = Perfiles.objects.get(usuario=request.user)
			nueva_cita.creador = perfil_usuario
			nueva_cita.save()
			return HttpResponseRedirect(reverse('citas:index'))
		else:
			pass #!!! enviar errores
	else:
		form = FormNuevaCita()
		context = {'FormNuevaCita':FormNuevaCita}
		return render(request, 'citas/nueva.html', context)

def marcar_favorito(request, cita_id):
	cita = Cita.objects.get(pk=cita_id)
	perfil_usuario = Perfiles.objects.get(usuario=request.user)
	#revisa si ya marco como favorito a esa cita
	fue_eliminado = False
	registro_existe = Cfavoritas.objects.filter(cita=cita, perfil = perfil_usuario).exists()
	if registro_existe:
		print 1
		registro_favorito = Cfavoritas.objects.get(cita=cita, perfil = perfil_usuario)
		fue_eliminado = registro_favorito.eliminado
		if fue_eliminado == True:
			print 2
			cita.favoritos_recibidos += 1
			registro_favorito.eliminado = False
			cita.save()
			registro_favorito.save()
			return HttpResponseRedirect(reverse('citas:index'))
		else:
			print 3
			cita.favoritos_recibidos -= 1
			registro_favorito.eliminado = True
			cita.save()
			registro_favorito.save()
			return HttpResponseRedirect(reverse('citas:index'))
	else:
		print 4
		cita.favoritos_recibidos += 1
		registro_favorito = Cfavoritas(cita=cita, perfil = perfil_usuario)
		registro_favorito.save()
		cita.save()
		return HttpResponseRedirect(reverse('citas:index'))

def favoritas(request):
	perfil_usuario = Perfiles.objects.get(usuario=request.user)
	Cfavoritas_objects = Cfavoritas.objects.filter(perfil = perfil_usuario).order_by('-fecha')
	citas_favoritas = []
	for c in Cfavoritas_objects:
		citas_favoritas.append(c.cita)

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

	context = {'citas_favoritas':citas_favoritas, 'imagenes_display': imagenes_display,
	'primera_imagen':primera_imagen}
	
	return render(request, 'citas/favoritas.html', context)

def colaborar_organizar(request):
	citas_eliminadas = Cita.objects.filter(eliminada=True, removidatotalmente = False)
	tabla_citas = []
	for cita in citas_eliminadas:
		frase = [cita.texto, cita.autor, cita.fuente, cita.id]
		correcciones = []
		if Ceditadas.objects.filter(cita=cita).exists():
			correcciones_objects = Ceditadas.objects.filter(cita=cita)
			for c in correcciones_objects:
				fecha = c.fecha
				razon = c.razon
				perfil = c.perfil.usuario.username
				correccion = [fecha, razon, perfil]
				correciones.append(correcion)
		color = ""
		estado = []
		vistos = cita.vistos_recibidos
		x = cita.xrecibidas
		estado_num = vistos - x
		if estado_num > 0:
			color = "success"
			if estado_num == 1:
				estado.append(["ok"])
			else:
				estado.append(["ok", "ok"])
		elif estado_num < 0:
			color = "danger"
			if estado_num == -1:
				estado.append(["remove"])
			else:
				estado.append(["remove", "remove"])
		else:
			color = "warning"
			estado.append(["flag"])
		tabla_citas.append([frase, correcciones, estado, color])

	#variables y calculo del progress bar
	vistos_totales = citas_eliminadas.aggregate(Sum('vistos_recibidos'))
	x_totales = citas_eliminadas.aggregate(Sum('xrecibidas'))
	suma_x_vistos = vistos_totales['vistos_recibidos__sum'] + x_totales['xrecibidas__sum']
	max_posible = citas_eliminadas.count()*3
	porcentaje_avanzado = (float(suma_x_vistos)/float(max_posible))*100
	progress_bar = str(porcentaje_avanzado)

	context = {'tabla_citas':tabla_citas, 'progress_bar':progress_bar}
	return render(request, 'citas/citas_coorg.html', context)

def denunciar_cita(request, cita_id):
	cita_denunciada = Cita.objects.get(id=cita_id)
	cita_denunciada.denunciada += 1
	if cita_denunciada.denunciada >= 3:
		cita_denunciada.eliminada = True
	cita_denunciada.save()
	return redirect('citas:index')

def marcar_visto(request, cita_id):
	#!!! falta limitar a un visto por usuario con una nueva tabla
	cita = Cita.objects.get(id=cita_id)
	if cita.xrecibidas > 0:
		cita.xrecibidas -= 1
	else:
		cita.vistos_recibidos += 1
		if cita.vistos_recibidos >= 3:
			cita.eliminada = False
			cita.vistos_recibidos = 0
			cita.denunciada = 0
	cita.save()
	return redirect('citas:colaborar_organizar')

def marcar_x(request, cita_id):
	#!!! falta limitar a una x por usuario con una nueva tabla
	cita = Cita.objects.get(id=cita_id)
	if cita.vistos_recibidos > 0:
		print "aca"
		cita.vistos_recibidos -= 1
	else:
		cita.xrecibidas += 1
		if cita.xrecibidas >= 3:
			cita.removidatotalmente = True
			cita.xrecibidas = 0
			cita.denunciada = 0
	cita.save()
	return redirect('citas:colaborar_organizar')






 





