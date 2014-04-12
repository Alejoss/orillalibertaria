# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Sum

from endless_pagination.decorators import page_template
from models import Cita, Cfavoritas, Ceditadas
from perfiles.models import Perfiles
from forms import FormNuevaCita, FormEditarCita
from imagenes.models import Imagen

# Create your views here.
@page_template('index_page_citas.html')
def index(request, queryset, template = 'citas/index.html', extra_context = None):
	autor = ""
	recientes = ""
	populares = ""
	q = ""
	if queryset == "autor":
		q = "autor"
		autor = "active"
	elif queryset == "populares":
		q = "-favoritos_recibidos"
		populares = "active"
	else:
		q = "-fecha"
		recientes = "active"

	citas = Cita.objects.filter(eliminada=False).order_by(q)

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

	context = {'citas': citas, 'imagenes_display': imagenes_display, 'primera_imagen':primera_imagen,
	'autor':autor, 'recientes':recientes, 'populares':populares}

	if extra_context is not None:
		context.update(extra_context)
		
	return render(request, template, context)

def nueva(request):
	template = 'citas/nueva.html'
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

	lista_de_autores = []
	lista_de_autores_obj = Cita.objects.filter(eliminada=False).values('autor').order_by('autor')
	for x in lista_de_autores_obj:
		if x['autor'] not in lista_de_autores:
			lista_de_autores.append(x['autor'])

	form = FormNuevaCita()
	context = {'FormNuevaCita':FormNuevaCita, 
	'lista_de_autores':lista_de_autores}
	return render(request,template, context)

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
			return HttpResponseRedirect(reverse('citas:index', kwargs={'queryset':u'recientes'}))
		else:
			print 3
			cita.favoritos_recibidos -= 1
			registro_favorito.eliminado = True
			cita.save()
			registro_favorito.save()
			return HttpResponseRedirect(reverse('citas:index', kwargs={'queryset':u'recientes'}))
	else:
		print 4
		cita.favoritos_recibidos += 1
		registro_favorito = Cfavoritas(cita=cita, perfil = perfil_usuario)
		registro_favorito.save()
		cita.save()
		return HttpResponseRedirect(reverse('citas:index', kwargs={'queryset':u'recientes'}))

def favoritas(request, username):
	template = 'citas/favoritas.html'
	user_object = User.objects.get(username=username)
	perfil_usuario = Perfiles.objects.get(usuario=user_object)

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

	propio_usuario = False
	if request.user == user_object:
		propio_usuario = True

	context = {'citas_favoritas':citas_favoritas, 'imagenes_display': imagenes_display,
	'primera_imagen':primera_imagen, 'user_object':user_object, 'propio_usuario':propio_usuario}
	
	return render(request, template , context)

def colaborar_organizar(request):
	template = 'citas/citas_coorg.html'
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
				correcciones.append(correccion)
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
	return render(request, template , context)

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

def coorg_editar(request, cita_id):
	template = 'citas/editar_cita.html'
	cita = Cita.objects.get(id=cita_id)
	perfil_usuario = Perfiles.objects.get(usuario = request.user)
	if request.method == 'POST':
		form = FormEditarCita(request.POST)
		if form.is_valid():
			texto = form.cleaned_data['texto']
			autor = form.cleaned_data['autor']
			fuente = form.cleaned_data['fuente']
			razon = form.cleaned_data['razon']
			if texto != cita.texto:
				cita.texto = texto
			if autor != cita.autor:
				cita.autor = autor
			if fuente != cita.fuente:
				cita.fuente = fuente
			cita.save()
			ceditadas_obj = Ceditadas(cita=cita, perfil = perfil_usuario, razon = razon)
			ceditadas_obj.save()
			return redirect('citas:colaborar_organizar')
		else:
			form_editar_cita = FormEditarCita(initial={'texto':cita.texto, 
				'autor':cita.autor, 'fuente':cita.fuente}) 
			#!!! enviar errores

	else:
		form_editar_cita = FormEditarCita(initial={'texto':cita.texto, 
				'autor':cita.autor, 'fuente':cita.fuente})

	context = {'form_editar_cita':form_editar_cita, 'cita_id':cita_id}
	return render(request,template , context)








 





