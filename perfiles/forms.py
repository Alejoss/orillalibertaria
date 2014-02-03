
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from models import Perfiles

class FormRegistroUsuario(UserCreationForm):
	email = forms.EmailField(required = True) #añade un email al default UserCreationForm
	
	class Meta:
		model = User
		#define los fields que se pasaran a registrar.html
		fields = ('username', 'email', 'password1', 'password2')

	def save(self, commit = True):
		#crea un objecto listo para salvar pero frena el save()
		user = super(FormRegistroUsuario, self).save(commit=False)
		#añade el email de cleaned data al objecto User que se va a salvar
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

class PerfilesForm(forms.ModelForm):

	class Meta:
		model = Perfiles
		#fields para el form de editar_perfil
		fields = ('descripcion', 'link1','link2','link3','link4',
			'link5','link6','link7','link8','link9','link10')


class UserForm(forms.Form):
	email = forms.EmailField(required=False)
	first_name = forms.CharField(max_length = 255, required = False)
	last_name = forms.CharField(max_length = 255, required = False)

