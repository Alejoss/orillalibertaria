# -*- coding: utf-8 -*-
from models import Imagen
from django import forms

class FormNuevaImagen(forms.ModelForm):
	class Meta:
		model = Imagen
		fields = ('url',)