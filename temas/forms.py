# -*- coding: utf-8 -*-
import bleach

from models import Posts
from django import forms
from django.forms import Textarea, TextInput
from django.utils import html


class FormCrearTema(forms.Form):
    # class form-control es para Bootstrap.
    # wchar_min es para control de caracteres en el input
    nombre = forms.CharField(max_length=50, widget=TextInput(attrs={
        'class': 'form-control'
        }))
    texto = forms.CharField(
        label="Descripción", max_length=1000, required=False,
        widget=forms.Textarea(attrs={
            'data-maxlength': 1000,
            'class': 'form-control',
            'id': 'wchar_min',
            'rows': 3,
        }))
    imagen = forms.CharField(label="Imagen", max_length=250, required=False,
                             widget=TextInput(attrs={'class': 'form-control'}))

    # remover todo tipo de html tags del texto por seguridad
    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])

        return texto_limpio


class FormNuevoPost(forms.ModelForm):

    class Meta:
        model = Posts
        fields = ('texto',)
        labels = {
            'texto': ''
        }

        widgets = {
            'texto': Textarea(attrs={
                'rows': 2,
                'max-length': 10000,
                'class': 'form-control',
            })
        }

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio


class FormEditarTema(forms.Form):
    descripcion = forms.CharField(label="Descripción", max_length=1000,
                                  required=False, help_text="edita la descripción del tema.",
                                  widget=forms.Textarea(attrs={
                                      'data-maxlength': 1000,
                                      'rows': 5,
                                      'class': 'form-control',
                                      'id': 'wchar_min'
                                  }))
    imagen = forms.CharField(label="Imagen", max_length=250, required=False,
                             widget=TextInput(attrs={'class': 'form-control'}))

    def clean_texto(self):
        texto = self.cleaned_data['descripcion']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio


class FormEditarPost(forms.Form):
    texto = forms.CharField(label="Post", max_length=1000, required=False,
                            widget=forms.Textarea(attrs={
                                'data-maxlength': 1000,
                                'rows': 5,
                                'class': 'form-control'
                            }))

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio
