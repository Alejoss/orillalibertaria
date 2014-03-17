# -*- coding: utf-8 -*-
 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib import auth

from forms import FormRegistroUsuario, PerfilesForm, UserForm
from models import Perfiles
from temas.models import Posts
from citas.models import Cita, Cfavoritas
from imagenes.models import Imagen, Ifavoritas

# print "nombre variable: %s" %(nombre variable) -- print para debug una variable
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
		return redirect('temas:main')
	else:
		return redirect('perfiles:login')
	
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
			user = User.objects.get(username=form.cleaned_data['username'])
			perfil_nuevo = Perfiles(usuario = user)
			perfil_nuevo.save()
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
	user = request.user
	#crea una tabla de Perfiles para el user
	#si no existe una ya y obtiene esa tabla como "obj"
	obj, created = Perfiles.objects.get_or_create(usuario = user)
	perfil_usuario = Perfiles.objects.get(usuario=user)
	tiene_imagenesfav = Ifavoritas.objects.filter(perfil=perfil_usuario).exists()
	tiene_frasesfav = Cfavoritas.objects.filter(perfil=perfil_usuario).exists()
	if request.method == 'POST':
		form = PerfilesForm(request.POST)
		if form.is_valid():
			#una vez validado el form. Recoge el user guardado en request (loggeado)
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
			return redirect('perfiles:perfil', username = request.user.username)
		else:
			#Si el form no es válido, un nuevo unbound form en "editar_perfil_form"
			error = "error en form.is_valid" #!!! Falta enviar errores.
	
	editar_perfil_form = PerfilesForm()
	context = {'editar_perfil_form':editar_perfil_form, 'tiene_imagenesfav':tiene_imagenesfav,
	'tiene_frasesfav':tiene_frasesfav}
	return render(request, 'perfiles/editar_perfil_des.html', context)
		
def editar_perfil_info(request):
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
	return render(request, 'perfiles/editar_perfil_info.html', context)

def perfil(request, username):
	#funciona cuando se visita el perfil de otro usuario
	#recibe del urlpattern un "username"
	#obtiene el User correspondiende a ese username
	usuario_user = User.objects.get(username=username)
	#obtiene el Perfiles correspondiente al User
	usuario_perfil = Perfiles.objects.get(usuario=usuario_user)
	nombre_completo = usuario_user.get_full_name()
	posts = Posts.objects.filter(creador=usuario_perfil).order_by('-fecha')
	posts_populares = Posts.objects.filter(creador=usuario_perfil, votos_positivos__gt=1).order_by('votos_positivos')
	citas_favoritas = Cfavoritas.objects.filter(perfil=usuario_perfil, eliminado = False)
	
	portada = ""
	imagenes_favoritas = []
	tiene_imagenesfav = Ifavoritas.objects.filter(perfil=usuario_perfil).exists()

	if tiene_imagenesfav:
		numero_imgfavoritas = Ifavoritas.objects.filter(perfil=usuario_perfil).count()
		if numero_imgfavoritas > 10:
			numero_imgfavoritas = 10		
		ifavoritas_objects = Ifavoritas.objects.filter(perfil=usuario_perfil, eliminado=False, portada=False).order_by('fecha')[:numero_imgfavoritas]
		for i in ifavoritas_objects:
			print "perfiles views - i.imagen.url: %s" %(i.imagen.url)
			imagenes_favoritas.append(i.imagen.url)
		if Ifavoritas.objects.filter(perfil=usuario_perfil, portada=True).exists():
			portada_obj = Ifavoritas.objects.get(perfil=usuario_perfil, eliminado = False, portada=True)
		else:
			portada_obj = Ifavoritas.objects.filter(perfil=usuario_perfil, eliminado=False).latest('id')
		portada = portada_obj.imagen.url
	#usuario al que se le va a redirigir cuando de click en "Ver todas"
	usuario_fav = usuario_user.username 

	context = {'portada':portada,'usuario_user': usuario_user, 'usuario': usuario_perfil, 
	'nombre_completo': nombre_completo, 'posts':posts, 'posts_populares':posts_populares,
	'citas_favoritas':citas_favoritas, 'imagenes_favoritas':imagenes_favoritas, 
	'usuario_fav':usuario_fav, 'tiene_imagenesfav':tiene_imagenesfav}
	#renderea perfiles.html con el user y el perfil correspondiente
	return render(request, 'perfiles/perfil.html', context)


def index(request):
	#pagina principal de usuarios. Muestra los usuarios.
	#En el futuro mostrar actividad 
	usuarios = Perfiles.objects.all()
	return render(request, 'perfiles/index.html', {'usuarios': usuarios})
