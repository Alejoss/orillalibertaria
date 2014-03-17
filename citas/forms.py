# -*- coding: utf-8 -*-
from models import Cita
from django import forms


class FormNuevaCita(forms.ModelForm):
	fuente = forms.CharField(required=False)
	class Meta:
		model = Cita
		fields = ('texto', 'autor', 'fuente')

class FormEditarCita(forms.Form):
	texto = forms.CharField(max_length=500, widget=forms.Textarea)
	autor = forms.CharField(max_length=150, required=False)
	fuente = forms.CharField(max_length=150, required=False)
	razon = forms.CharField(
		widget=forms.TextInput(attrs={'placeholder':"¿Qué es lo que estaba mal?"}))
