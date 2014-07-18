# -*- coding: utf-8 -*-
from models import Cita
from django import forms
from django.forms import ModelForm, Textarea, TextInput
from django.utils import html


class FormNuevaCita(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FormNuevaCita, self).__init__(*args, **kwargs)
        self.fields['fuente'].required = False
        self.fields['autor'].required = True
        self.fields['texto'].required = True

    class Meta:
        model = Cita
        fields = ('texto', 'autor', 'fuente')
        widgets = {
            'texto': Textarea(attrs={'rows': 3, 'data-maxlength': 1000,
                                     'class': 'form-control',
                                     'id': 'wchar'}),
            'autor': TextInput(attrs={'class': 'form-control'}),
            'fuente': TextInput(attrs={'class': 'form-control'})
        }

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio = html.strip_tags(texto)
        return texto_limpio


class FormEditarCita(forms.Form):
    texto = forms.CharField(max_length=1000, widget=Textarea(attrs={'class': 'form-control', 'id': 'wchar'}))
    autor = forms.CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'form-control'}))
    fuente = forms.CharField(max_length=150, required=False, widget=TextInput(attrs={'class': 'form-control'}))
    razon = forms.CharField(
        widget=TextInput(attrs={'class': "form-control", 'placeholder': '¿Qué es lo que estaba mal?'}))

    def clean_texto(self):
        texto = self.cleaned_data['texto']
        texto_limpio = html.strip_tags(texto)
        return texto_limpio
