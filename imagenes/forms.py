# -*- coding: utf-8 -*-
from django import forms
from django.forms import TextInput


class FormNuevaImagen(forms.Form):
    # class form-control es para Bootstrap.
    url = forms.URLField(max_length=200, widget=TextInput(attrs={'class': 'form-control'}))
    favorita = forms.BooleanField(initial=False, required=False)
