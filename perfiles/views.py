# -*- coding: utf-8 -*-
import random
 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth

from endless_pagination.decorators import page_template

from forms import FormRegistroUsuario, PerfilesForm, UserForm
from models import Perfiles
from temas.models import Posts, Respuestas, Votos
from citas.models import Cita, Cfavoritas
from imagenes.models import Imagen, Ifavoritas

# print "nombre variable: %s" %(nombre variable) -- print para debug una variable
# Create your views here.
def login_page(request):
	template = 'perfiles/login.html'
	#Custom login. No es el login normal de Django.
	return render(request, template)

def authcheck(request):
	#standard auth de Django.
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password = password)
	#busca en la bd User uno que existe con ese usuario y password
	if user is not None:
		#Si existe, hace login a ese usuario y lo guarda en "request"
		auth.login(request, user)
		return redirect('temas:main', 'recientes')
	else:
		return redirect('perfiles:login')
	
def logout(request):
	template = 'perfiles/logout.html'

	auth.logout(request) # Logout el user guardado en Request
	return render(request, template , {})

def loggedin(request):
	template = 'perfiles/loggedin.html'
	#Mensaje de Bienvenida. 
	#!!! En el futuro redireccionar (despues de 3 seg) a dnd estaba antes (next)
	#o a la página de Temas
	return render(request, template, {})

def invalid(request):
	#Invalid login. Esta pagina hay que eliminar. 
	#Debe ser la misma que login pero con mensajes de error.
	context = {}
	return render(request, 'perfiles/invalid.html', {})

def registrar(request):
	template = 'perfiles/registrar.html'
	#Registra nuevos usuarios.
	error = ""#Hay que eliminar esta variable y cambiar por los errors del form.
	if request.method == 'POST':
		#Recoge el form de forms.py y le asigna las variables del 
		#diccionario de request.POST
		form = FormRegistroUsuario(request.POST) 
		#valida el form conforme a las reglas preestablecidas en form.py
		if form.is_valid():
			form.save() #Guarda los valores en la base de datos auth.User.
			user = User.objects.get(username=form.cleaned_data['username'])
			perfil_nuevo, created = Perfiles.objects.get_or_create(usuario = user)
			perfil_nuevo.save()
			return HttpResponseRedirect(reverse('perfiles:registro_ok'))
		else:
			error = "error en form.is_valid" #!!!
	#Crea un nuevo form vacio. (unbound)
	user_creation_form = FormRegistroUsuario()
	context = {'user_creation_form': user_creation_form, 'error':error}
	return render(request, template, context)

def registro_ok(request):

	#Lleva a una página de Bienvenida.
	context = {}
	return render(request, 'perfiles/registro_ok.html', context)

def editar_perfil_des(request):
	template = 'perfiles/editar_perfil_des.html'

	user = request.user
	#crea una tabla de Perfiles para el user
	#si no existe una ya y obtiene esa tabla como "obj"
	perfil_usuario, created = Perfiles.objects.get_or_create(usuario = user)
	tiene_imagenesfav = Ifavoritas.objects.filter(perfil=perfil_usuario).exists()
	tiene_frasesfav = Cfavoritas.objects.filter(perfil=perfil_usuario).exists()
	if request.method == 'POST':
		form = PerfilesForm(request.POST)
		if form.is_valid():
			#una vez validado el form. Recoge el user guardado en request (loggeado)
			#Llena los valores del obj con los valores del form request.Post.
			descripcion = form.cleaned_data.get('descripcion')
			link1 = form.cleaned_data.get('link1')
			link2 = form.cleaned_data.get('link2')
			link3 = form.cleaned_data.get('link3')
			link4 = form.cleaned_data.get('link4')
			link5 = form.cleaned_data.get('link5')
			perfil_usuario.link1 = link1
			perfil_usuario.link2 = link2
			perfil_usuario.link3 = link3
			perfil_usuario.link4 = link4
			perfil_usuario.link5 = link5
			if len(descripcion)>5:
				perfil_usuario.descripcion = descripcion
			perfil_usuario.save()
			#Redirije al perfil del usuario. pasa el username como
			#kwargs para manejo de urlpattern
			return redirect('perfiles:perfil', username = request.user.username)
		else:
			#Si el form no es válido, un nuevo unbound form en "editar_perfil_form"
			error = "error en form.is_valid" #!!! Falta enviar errores.
	
	editar_perfil_form = PerfilesForm(initial={
		'link1':perfil_usuario.link1, 'link2':perfil_usuario.link2,
		'link3':perfil_usuario.link3, 'link4':perfil_usuario.link4,
		'link5':perfil_usuario.link5})

	context = {'editar_perfil_form':editar_perfil_form, 
	'tiene_imagenesfav':tiene_imagenesfav,
	'tiene_frasesfav':tiene_frasesfav,
	'perfil_usuario':perfil_usuario}
	return render(request, template, context)
		
def editar_perfil_info(request):
	template = 'perfiles/editar_perfil_info.html'

	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			obj = User.objects.get(username=request.user.username)
			e = form.cleaned_data['email']
			f = form.cleaned_data['first_name']
			l = form.cleaned_data['last_name']
			if e != "":
				obj.email = e

			if f != "":
				obj.first_name = f

			if l != "":
				obj.last_name = l
			
			obj.save()
			return redirect('perfiles:perfil', username = request.user.username)
		else:
			pass #!!! enviar errores	
	
	perfil_info_form = UserForm()
	context = {'perfil_info_form': perfil_info_form}
	return render(request, template, context)

@page_template('index_page_perfiles.html')
def perfil(request, username, queryset, template = "perfiles/perfil.html",
	extra_context = None):
	#funciona cuando se visita el perfil de otro usuario
	#recibe del urlpattern un "username y un queryset.
	#obtiene el User correspondiende a ese username
	usuario_user = User.objects.get(username=username)
	#obtiene el Perfiles correspondiente al User
	usuario_perfil = Perfiles.objects.get(usuario=usuario_user)
	nombre_completo = usuario_user.get_full_name()

	recientes = ""
	populares = ""
	q = ""
	if queryset == "populares":
		q = "-votos_positivos"
		populares = "active"
	else:
		q = "-fecha"
		recientes = "active"

	posts_obj = Posts.objects.filter(creador=usuario_perfil).order_by(q)
	posts = []
	for p in posts_obj:
		post = [p]
		if p.es_respuesta == True:
			if Respuestas.objects.filter(post_respuesta=p).exists():
				respuesta = Respuestas.objects.get(post_respuesta=p)
				usuario_respuesta = respuesta.post_padre.creador.usuario.username
				post.extend([True, usuario_respuesta])
			else:
				post.extend([False, ""]) #!!! Prueba para ver respuestas descuadradas.
		else:
			post.extend([False, ""])

		voted_status = "no-vote"
		if p.creador == request.user:
			voted_status = "propio_post"
		else:
			if Votos.objects.filter(post_votado=p, usuario_votante=request.user).exists():
				voto = Votos.objects.get(post_votado=p, usuario_votante=request.user)
				if voto.tipo == 1:
					voted_status = "voted-up"
				elif voto.tipo == -1:
					voted_status = "voted-down"
				else:
					voted_status = "no-vote"
					
		post.append(voted_status)
		posts.append(post)

	citas_favoritas_obj = Cfavoritas.objects.filter(perfil=usuario_perfil, eliminado = False)
	cita_favorita = (random.choice(citas_favoritas_obj)).cita

	portada = ""
	imagenes_favoritas = []
	tiene_imagenesfav = Ifavoritas.objects.filter(perfil=usuario_perfil).exists()

	if tiene_imagenesfav:
		numero_imgfavoritas = Ifavoritas.objects.filter(perfil=usuario_perfil).count()
		if numero_imgfavoritas > 3:
			numero_imgfavoritas = 3		
		ifavoritas_objects = Ifavoritas.objects.filter(perfil=usuario_perfil, eliminado=False, portada=False).order_by('-fecha')[:numero_imgfavoritas]
		for i in ifavoritas_objects:
			imagenes_favoritas.append(i.imagen.url)
		if Ifavoritas.objects.filter(perfil=usuario_perfil, portada=True).exists():
			portada_obj = Ifavoritas.objects.get(perfil=usuario_perfil, eliminado = False, portada=True)
		else:
			portada_obj = Ifavoritas.objects.filter(perfil=usuario_perfil, eliminado=False).latest('id')
		portada = portada_obj.imagen.url
	#usuario al que se le va a redirigir cuando de click en "Ver todas"
	usuario_fav = usuario_user.username 

	context = {'portada':portada,'usuario_user': usuario_user, 'usuario': usuario_perfil, 
	'nombre_completo': nombre_completo, 'posts':posts,'cita_favorita':cita_favorita,
	'imagenes_favoritas':imagenes_favoritas, 'usuario_fav':usuario_fav,
	'tiene_imagenesfav':tiene_imagenesfav, 'recientes':recientes, 'populares': populares}

	if extra_context is not None:
		context.update(extra_context)

	return render(request, template, context)

def index(request):
	template = 'perfiles/index.html'
	#pagina principal de usuarios. Muestra los usuarios.
	#En el futuro mostrar actividad 
	usuarios = Perfiles.objects.all()
	return render(request,template , {'usuarios': usuarios})
