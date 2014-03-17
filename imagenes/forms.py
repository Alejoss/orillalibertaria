# -*- coding: utf-8 -*-
from django import forms

class FormNuevaImagen(forms.Form):
	favorita = forms.BooleanField(initial=False, required=False)
	url = forms.CharField(max_length=200)
