
from django.db import models
from perfiles.models import Perfiles
# Create your models here.


class Temas(models.Model):
	nombre = models.CharField(max_length=100, null=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
	descripcion = models.CharField(max_length=250, blank = True, null=True)
	activo = models.BooleanField(default=True)
	creador = models.ForeignKey(Perfiles, null=True)

class Posts(models.Model):
	fecha = models.DateTimeField(auto_now_add = True)
	texto = models.TextField(max_length=10000, null=True)
	es_respuesta = models.BooleanField(default=False)
	votos_positivos = models.PositiveSmallIntegerField(default=0)
	votos_negativos = models.PositiveSmallIntegerField(default=0)
	creador = models.ForeignKey(Perfiles, null = True)
	tema = models.ForeignKey(Temas, null = True)

class Respuestas(models.Model):
	post_respuesta = models.ForeignKey(Posts, related_name = "respuesta", null=True)
	post_padre = models.ForeignKey(Posts, related_name = "post_original", null=True)


class Votos(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	usuario_votado = models.ForeignKey(Perfiles, related_name = 'votado', null=True)
	usuario_votante = models.ForeignKey(Perfiles, related_name = 'votante', null=True)
	post_votado = models.ForeignKey(Posts, null=True)
	tema = models.ForeignKey(Temas, null=True)
	tipo = models.SmallIntegerField(default=0)

	
class Notificaciones(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	usuario_id = models.ForeignKey(Perfiles, null=True)
	tipo_notificacion = models.CharField(max_length=50, null=True)
	leido = models.BooleanField(default=False)
	tema = models.ForeignKey(Temas, null=True)
	link = models.CharField(max_length=200, null=True)

class Mensajes(models.Model):
	fecha = models.DateTimeField(auto_now_add = True)
	usuario_envia = models.ForeignKey(Perfiles, related_name = 'envia', null=True)
	usuario_recibe = models.ForeignKey(Perfiles, related_name = 'recibe', null=True)
	mensaje = models.CharField(max_length = 1000, null=True)
	leido = models.BooleanField(default = False)
	deleted_inbox = models.BooleanField(default = False)
	deleted_sentbox = models.BooleanField(default = False)