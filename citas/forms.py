# -*- coding: utf-8 -*-
from models import Cita
from django import forms


class FormNuevaCita(forms.ModelForm):
	fuente = forms.CharField(required=False)
	class Meta:
		model = Cita
		fields = ('texto', 'autor', 'fuente')

