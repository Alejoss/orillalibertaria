# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from forms import FormRegistroUsuario, PerfilesForm, UserForm
from django.core.urlresolvers import reverse
from models import Perfiles
from temas.models import Posts
from django.contrib.auth.models import User



# Create your views here.
def login(request):
	#Custom login. No es el login normal de Django.
	return render(request, 'perfiles/login.html')

def authcheck(request):
	#standard auth de Django.
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password = password)
	#busca en la bd User uno que existe con ese usuario y password
	if user is not None:
		#Si existe, hace login a ese usuario y lo guarda en "request"
		auth.login(request, user)
		return render(request, 'perfiles/loggedin.html', {'username': username})
	else:
		return render(request, 'perfiles/invalid.html', {'username': username})
	
def logout(request):
	auth.logout(request) # Logout el user guardado en Request
	return render(request, 'perfiles/logout.html', {})

def loggedin(request):
	#Mensaje de Bienvenida. 
	#!!! En el futuro redireccionar (despues de 3 seg) a dnd estaba antes (next)
	#o a la página de Temas
	return render(request, 'perfiles/loggedin.html', {})

def invalid(request):
	#Invalid login. Esta pagina hay que eliminar. 
	#Debe ser la misma que login pero con mensajes de error.
	context = {}
	return render(request, 'perfiles/invalid.html', {})

def registrar(request):
	#Registra nuevos usuarios.
	error = ""#Hay que eliminar esta variable y cambiar por los errors del form.
	if request.method == 'POST':
		#Recoge el form de forms.py y le asigna las variables del 
		#diccionario de request.POST
		form = FormRegistroUsuario(request.POST) 
		#valida el form conforme a las reglas preestablecidas en form.py
		if form.is_valid():
			form.save() #Guarda los valores en la base de datos auth.User.
			return HttpResponseRedirect(reverse('perfiles:registro_ok'))
		else:
			error = "error en form.is_valid" #!!!
	#Crea un nuevo form vacio. (unbound)
	user_creation_form = FormRegistroUsuario()
	context = {'user_creation_form': user_creation_form, 'error':error}
	return render(request, 'perfiles/registrar.html', context)

def registro_ok(request):
	#Lleva a una página de Bienvenida.
	context = {}
	return render(request, 'perfiles/registro_ok.html', context)

def editar_perfil_des(request):
	if request.method == 'POST':
		form = PerfilesForm(request.POST)
		if form.is_valid():
			#una vez validado el form. Recoge el user guardado en request (loggeado)
			user = request.user
			#crea una tabla de Perfiles para el user
			#si no existe una ya y obtiene esa tabla como "obj"
			obj, created = Perfiles.objects.get_or_create(usuario = user)
			#Llena los valores del obj con los valores del form request.Post.
	
			def revisar_campo(campo):
				#revisa si el campo de cleaned data tiene mas de 4 caracteres
				if len(form.cleaned_data[campo])>4:
					return True
				else:
					return False

			if revisar_campo('descripcion'):
				obj.descripcion = form.cleaned_data['descripcion']
			if revisar_campo('link1'):
				obj.link1 = form.cleaned_data['link1']
			if revisar_campo('link2'):
				obj.link2 = form.cleaned_data['link2']
			if revisar_campo('link3'):
				obj.link3 = form.cleaned_data['link3']
			if revisar_campo('link4'):
				obj.link4 = form.cleaned_data['link4']
			if revisar_campo('link5'):
				obj.link5 = form.cleaned_data['link5']
			if revisar_campo('link6'):
				obj.link6 = form.cleaned_data['link6']
			if revisar_campo('link7'):
				obj.link7 = form.cleaned_data['link7']
			if revisar_campo('link8'):
				obj.link8 = form.cleaned_data['link8']
			if revisar_campo('link9'):
				obj.link9 = form.cleaned_data['link9']
			if revisar_campo('link10'):
				obj.link10 = form.cleaned_data['link10']

			obj.save()
			#Redirije al perfil del usuario. pasa el username como
			#kwargs para manejo de urlpattern
			HttpResponseRedirect(reverse('perfiles:perfil_propio'))
		else:
			#Si el form no es válido, un nuevo unbound form en "editar_perfil_form"
			error = "error en form.is_valid" #!!! Falta enviar errores.
	
	editar_perfil_form = PerfilesForm()
	context = {'editar_perfil_form':editar_perfil_form}
	return render(request, 'perfiles/editar_perfil_des.html', context)
		


def editar_perfil_info(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			obj = User.objects.get(username=request.user)
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
			return HttpResponseRedirect(reverse('perfiles:perfil_propio'))
		else:
			pass #!!! enviar errores	
	
	perfil_info_form = UserForm()
	context = {'perfil_info_form': perfil_info_form}
	return render(request, 'perfiles/editar_perfil_info.html', context)

def perfil_propio(request):
	#funciona cuando el usuario da click en su propio perfil.
	#guarda la tabla Perfiles del request.user en "usuario"
	if request.user.is_authenticated():
		usuario = Perfiles.objects.get(usuario=request.user)
		posts = Posts.objects.filter(creador=usuario)
		nombre_completo = request.user.get_full_name()
		context = {'usuario':usuario, 'posts': posts, 
		'nombre_completo':nombre_completo}
		#redirije a perfiles"perfil y pasa el usuario como kwargs para manejo del urlpattrn.
		return render(request, 'perfiles/perfil.html', context)
	else:
		return HttpResponseRedirect(reverse('perfiles:login'))

def perfil(request, username):
	#funciona cuando se visita el perfil de otro usuario
	#recibe del urlpattern un "username"
	print "llego al perfil de %s" %(username)
	#obtiene el User correspondiende a ese username
	usuario_user = User.objects.get(username=username)
	#obtiene el Perfiles correspondiente al User
	usuario_perfil = Perfiles.objects.get(usuario=usuario_user)
	nombre_completo = usuario_user.get_full_name()
	posts = Posts.objects.filter(creador=usuario_user)
	context = {'usuario_user': usuario_user, 'usuario': usuario_perfil, 
	'nombre_completo': nombre_completo, 'posts':posts}
	#renderea perfiles.html con el user y el perfil correspondiente
	return render(request, 'perfiles/perfil.html', context)


def index(request):
	#pagina principal de usuarios. Muestra los usuarios.
	#En el futuro mostrar actividad 
	usuarios = Perfiles.objects.all()
	return render(request, 'perfiles/index.html', {'usuarios': usuarios})
