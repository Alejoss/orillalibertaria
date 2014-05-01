# -*- coding: utf-8 -*-
from models import Temas, Posts, Votos, Notificaciones, Mensajes, Tema_descripcion
from django import forms
from django.forms import ModelForm, Textarea


class FormCrearTema(forms.Form):
	nombre = forms.CharField(max_length=100)
	texto = forms.CharField(label = "Descripción", max_length=1000, required=False,
		help_text="Añádele una descripción inicial al tema.", 
		widget=forms.Textarea(attrs={
				'rows':3,
				}))
	imagen = forms.CharField(label = "Imagen", max_length=250, required=False,
		help_text="Una url a una imagen que sirva de portada al tema.")

class FormNuevoPost(forms.ModelForm):
	class Meta:
		model = Posts
		fields = ('texto',)
		labels = {
		'texto': ''
		}

		widgets = {
			'texto': Textarea(attrs={
				'rows':2,
				})
		}

class FormEditarTema(forms.Form):
	descripcion = forms.CharField(label = "Descripción", max_length=1000,
		required=False, help_text="edita la descripción del tema.", 
		widget=forms.Textarea(attrs={
				'rows':5,
				}))
	imagen = forms.CharField(label = "Imagen", max_length=250, required=False,
		help_text="cambia la imagen del tema. Pega el url a una nueva imagen.")

class FormEditarPost(forms.Form):
	texto = forms.CharField(label="Post", max_length=1000, required=False, 
		help_text= "Después de editarlo serás redirigido a la página del post.", widget = forms.Textarea(attrs={'rows':5,}))