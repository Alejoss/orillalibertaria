# -*- coding: utf-8 -*-
from models import Posts
from django import forms
from django.forms import Textarea, TextInput


class FormCrearTema(forms.Form):
    nombre = forms.CharField(max_length=100, widget=TextInput(attrs={
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


class FormEditarPost(forms.Form):
    texto = forms.CharField(label="Post", max_length=1000, required=False,
                            widget=forms.Textarea(attrs={
                                'data-maxlength': 1000,
                                'rows': 5,
                                'class': 'form-control'
                            }))
