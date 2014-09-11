# -*- coding: utf-8 -*-
import bleach

from django.forms import Textarea, TextInput
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import html


class FormRegistroUsuario(UserCreationForm):
    # Form fuera de uso, usuarios se registran con Facebook Twitter y Google
    # añade un email al default UserCreationForm
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # define los fields que se pasaran a registrar.html
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        # crea un objecto listo para salvar pero frena el save()
        user = super(FormRegistroUsuario, self).save(commit=False)
        # añade el email de cleaned data al objecto User que se va a salvar
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        return user


class PerfilesForm(forms.Form):
    # class form-control es para Bootstrap.
    # id nickname es para ajax y revisar si ya existe ese nickname
    descripcion = forms.CharField(
        label="Descripción", max_length=250, required=False,
        widget=forms.Textarea(attrs={'data-maxlength': 250,
                                     'rows': 3,
                                     'class': 'form-control',
                                     'id': 'wchar_250'
                                     }))

    nickname = forms.CharField(label="nickname", max_length=75, required=True,
                               widget=TextInput(attrs={'class': 'form-control',
                                                       'id': 'nickname'}))

    email = forms.EmailField(required=False, max_length=75,
                             widget=TextInput(attrs={'class': 'form-control'}))
    link1 = forms.CharField(max_length=250, required=False,
                            widget=TextInput(attrs={'class': 'form-control'}))
    link2 = forms.CharField(max_length=250, required=False,
                            widget=TextInput(attrs={'class': 'form-control'}))
    link3 = forms.CharField(max_length=250, required=False,
                            widget=TextInput(attrs={'class': 'form-control'}))
    link4 = forms.CharField(max_length=250, required=False,
                            widget=TextInput(attrs={'class': 'form-control'}))
    link5 = forms.CharField(max_length=250, required=False,
                            widget=TextInput(attrs={'class': 'form-control'}))

    # remover todo tipo de html tags del texto por seguridad
    def clean_descripcion(self):
        texto = self.cleaned_data['descripcion']
        texto_limpio_parcial = html.strip_tags(texto)
        texto_limpio = bleach.clean(texto_limpio_parcial, tags=[])
        return texto_limpio


class UserForm(forms.Form):
    email = forms.EmailField(max_length=250, required=False,
                             widget=TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=250, required=False,
                                 widget=TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=250, required=False,
                                widget=TextInput(attrs={'class': 'form-control'}))
