from django import forms
from django.forms import Textarea, TextInput
from django.utils import html


class FormNuevoVideo(forms.Form):
    url = forms.URLField(initial='http://', max_length=250, widget=TextInput(
    	attrs={'class': 'form-control'}))
    titulo = forms.CharField(max_length=150, widget=TextInput(
    	attrs={'class': 'form-control'}))
    descripcion = forms.CharField(
        widget=Textarea(attrs={'rows': 3,
        	                      'data-maxlength': 1000,
        	                      'class': 'form-control',
        					           'id': 'wchar'}))

    def clean_texto(self):
        texto = self.cleaned_data['descripcion']
        texto_limpio = html.strip_tags(texto)
        return texto_limpio


class FormEditarVideo(forms.Form):
    url = forms.URLField(max_length=250, widget=TextInput(attrs={'class': 'form-control'}))
    titulo = forms.CharField(max_length=150, widget=TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(
        widget=Textarea(attrs={'rows': 3, 'data-maxlength': 500, 'class': 'form-control',
                               'id': 'wchar'}))

    def clean_texto(self):
        texto = self.cleaned_data['descripcion']
        texto_limpio = html.strip_tags(texto)
        return texto_limpio
