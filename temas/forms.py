# -*- coding: utf-8 -*-
from models import Temas, Posts, Votos, Notificaciones, Mensajes, Tema_descripcion
from django import forms


class FormCrearTema(forms.Form):
	nombre = forms.CharField(max_length=100)
	texto = forms.CharField(max_length=1000, required=False)
	imagen = forms.CharField(max_length=250, required=False)

class FormNuevoPost(forms.ModelForm):
	class Meta:
		model = Posts
		fields = ('texto',)

class FormEditarTema(forms.Form):
	descripcion = forms.CharField(max_length=1000, required=False)
	imagen = imagen = forms.CharField(max_length=250, required=False)