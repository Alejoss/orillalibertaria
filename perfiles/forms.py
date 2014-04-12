# -*- coding: utf-8 -*-
from django.forms import ModelForm, Textarea
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

class PerfilesForm(forms.Form):
	
	descripcion = forms.CharField(label = "Descripción", max_length=250, required=False,
		help_text="Quién eres en los clásicos 250 caracteres.", 
		widget=forms.Textarea(attrs={
				'rows':3,
				}))
	link1 = forms.CharField(label = "Links:", required=False)
	link2 = forms.CharField(label= "", required = False)
	link3 = forms.CharField(label= "", required = False)
	link4 = forms.CharField(label= "", required = False)
	link5 = forms.CharField(label= "", required = False, 
		help_text="Comparte cinco links que digan algo sobre ti.")

class UserForm(forms.Form):
	email = forms.EmailField(required=False)
	first_name = forms.CharField(max_length = 255, required = False)
	last_name = forms.CharField(max_length = 255, required = False)

