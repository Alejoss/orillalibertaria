# -*- coding: utf-8 -*-
import bleach

from models import Cita
from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils import html


class FormNuevaCita(forms.ModelForm):
        # class form-control es para Bootstrap.
        # id wchar es para jquery, contar los caracteres.

    def __init__(self, *args, **kwargs):
        super(FormNuevaCita, self).__init__(*args, **kwargs)
        self.fields['fuente'].required = False  # La fuente no debe ser requerida
        self.fields['autor'].required = True
        self.fields['texto'].required = True

    class Meta:
        model = Cita
        fields = ('texto', 'autor', 'fuente')
        widgets = {
            'texto': Textarea(attrs={'rows': 3, 'data-maxlength': 1000,
                                     'class': 'form-control',
                                     'id': 'wchar'}),
            'autor': TextInput(attrs={'id': 'autor', 'class': 'form-control'}),
            'fuente': TextInput(attrs={'class': 'form-control'})
        }

    # remover todo tipo de html tags del texto por seguridad
    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio

    def clean_autor(self):
        autor = self.cleaned_data['autor']
        autor_limpio_parcial = html.strip_tags(autor)
        autor_limpio = bleach.clean(autor_limpio_parcial, tags=[])
        return autor_limpio

    def clean_fuente(self):
        fuente = self.cleaned_data['fuente']
        fuente_limpio_parcial = html.strip_tags(fuente)
        fuente_limpio = bleach.clean(fuente_limpio_parcial, tags=[])
        return fuente_limpio


class FormEditarCita(forms.Form):
    texto = forms.CharField(max_length=1000, widget=Textarea(attrs={'class': 'form-control', 'id': 'wchar'}))
    autor = forms.CharField(max_length=150, required=False,
                            widget=TextInput(attrs={'class': 'form-control',
                                                    'id': 'autor'}))  # id autor es para autocomplete
    fuente = forms.CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'form-control'}))
    razon = forms.CharField(
        widget=TextInput(attrs={'class': "form-control", 'placeholder': '¿Qué es lo que estaba mal?'}))

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio

    def clean_autor(self):
        autor = self.cleaned_data['autor']
        autor_limpio_parcial = html.strip_tags(autor)
        autor_limpio = bleach.clean(autor_limpio_parcial, tags=[])
        return autor_limpio

    def clean_fuente(self):
        fuente = self.cleaned_data['fuente']
        fuente_limpio_parcial = html.strip_tags(fuente)
        fuente_limpio = bleach.clean(fuente_limpio_parcial, tags=[])
        return fuente_limpio
