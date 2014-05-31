# -*- coding: utf-8 -*-
from models import Cita
from django import forms
from django.forms import ModelForm, Textarea


class FormNuevaCita(forms.ModelForm):
    #fuente = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(FormNuevaCita, self).__init__(*args, **kwargs)
        self.fields['fuente'].required = False

    class Meta:
        model = Cita
        fields = ('texto', 'autor', 'fuente')
        widgets = {
            'texto': Textarea(attrs={'rows': 3, 'data-maxlength': 500})
        }
        labels = {
            'texto': 'Frase'
        }
        help_texts = {
            'fuente': 'Libro, artículo, video, audio',
        }


class FormEditarCita(forms.Form):
    texto = forms.CharField(max_length=500, widget=forms.Textarea,
                            help_text='No pongas comillas, se añaden automáticamente.')
    autor = forms.CharField(max_length=150, required=False)
    fuente = forms.CharField(max_length=150, required=False)
    razon = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': "¿Qué es lo que estaba mal?"}))
