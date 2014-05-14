from django import forms

class FormNuevoVideo(forms.Form):
	url = forms.URLField(initial='http://')
	titulo = forms.CharField()
	descripcion = forms.CharField()
