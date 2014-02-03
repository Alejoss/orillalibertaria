# -*- coding: utf-8 -*-
from models import Temas, Posts, Votos, Notificaciones, Mensajes
from django import forms


class FormCrearTema(forms.ModelForm):
	class Meta:
		model = Temas
		fields = ('nombre', 'descripcion')

class FormNuevoPost(forms.ModelForm):
	class Meta:
		model = Posts
		fields = ('texto',)
