from django import forms
from django.forms import Textarea


class FormNuevoVideo(forms.Form):
    url = forms.URLField(initial='http://', max_length=250)
    titulo = forms.CharField(max_length=150)
    descripcion = forms.CharField(
        help_text="Describe el video para Orilla Libertaria",
        widget=Textarea(attrs={'rows': 3, 'data-maxlength': 500}))
