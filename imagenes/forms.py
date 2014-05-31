# -*- coding: utf-8 -*-
from django import forms


class FormNuevaImagen(forms.Form):
    url = forms.URLField(max_length=200)
    favorita = forms.BooleanField(initial=False, required=False,
                                  help_text="Sumar esta imagen a mis favoritas")
