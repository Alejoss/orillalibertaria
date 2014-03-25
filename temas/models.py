
from django.db import models
from django.template import defaultfilters
from perfiles.models import Perfiles
# Create your models here.
 

class Temas(models.Model):
	nombre = models.CharField(max_length=100, null=True)
	slug = models.SlugField(max_length=100, null = True)
	fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
	activo = models.BooleanField(default=True)
	creador = models.ForeignKey(Perfiles, null=True)
	nivel_actividad = models.SmallIntegerField(default=0)
	nivel_popularidad = models.SmallIntegerField(default=0)
	imagen = models.CharField(max_length=250, null = True)

	def __unicode__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = defaultfilters.slugify(self.nombre)
		super(Temas, self).save(*args, **kwargs)
 
class Posts(models.Model):
	fecha = models.DateTimeField(auto_now_add = True)
	texto = models.TextField(max_length=10000, null=True)
	es_respuesta = models.BooleanField(default=False)
	votos_positivos = models.PositiveSmallIntegerField(default=0)
	votos_negativos = models.PositiveSmallIntegerField(default=0)
	creador = models.ForeignKey(Perfiles, null = True)
	tema = models.ForeignKey(Temas, null = True)
	eliminado = models.BooleanField(default=False)

	def __unicode__(self):
		return "%s... en %s" %(self.texto[:20], self.tema.nombre)

class Respuestas(models.Model):
	post_respuesta = models.ForeignKey(Posts, related_name = "respuesta", null=True)
	post_padre = models.ForeignKey(Posts, related_name = "post_original", null=True)

	def __unicode__(self):
		return "%s... en respuesta a %s..., tema %s" %(self.post_respuesta.texto[:20], 
			self.post_padre.texto[:20], self.post_padre.tema.nombre )

class Votos(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	usuario_votado = models.ForeignKey(Perfiles, related_name = 'votado', null=True)
	usuario_votante = models.ForeignKey(Perfiles, related_name = 'votante', null=True)
	post_votado = models.ForeignKey(Posts, null=True)
	tema = models.ForeignKey(Temas, null=True)
	tipo = models.SmallIntegerField(default=0)

	def __unicode__(self):
		return "%s a favor de %s... en %s" %(self.usuario_votante.usuario.username,
			self.post_votado.texto[:20], self.tema.nombre)

class Notificaciones(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	usuario_id = models.ForeignKey(Perfiles, null=True) #!!!cambiar nombre a usuario
	tipo_notificacion = models.CharField(max_length=50, null=True)
	leido = models.BooleanField(default=False)
	tema = models.ForeignKey(Temas, null=True)
	link = models.CharField(max_length=200, null=True)

	def __unicode__(self):
		return "%s para %s el %s" %(self.tipo_notificacion, self.usuario_id, self.fecha)

class Mensajes(models.Model):
	fecha = models.DateTimeField(auto_now_add = True)
	usuario_envia = models.ForeignKey(Perfiles, related_name = 'envia', null=True)
	usuario_recibe = models.ForeignKey(Perfiles, related_name = 'recibe', null=True)
	mensaje = models.CharField(max_length = 1000, null=True)
	leido = models.BooleanField(default = False)
	deleted_inbox = models.BooleanField(default = False)
	deleted_sentbox = models.BooleanField(default = False)

	def __unicode__(self):
		return "mnsg de %s a %s el %s" %(self.usuario_envia.usuario.username,
			self.usuario_recibe.usuario.username, self.fecha)

class Tema_descripcion(models.Model):
	fecha = models.DateTimeField(auto_now_add=True)
	tema = models.ForeignKey(Temas)
	usuario = models.ForeignKey(Perfiles)
	texto = models.CharField(max_length=1000, blank=True, null=True)

	def __unicode__(self):
		return "descripcion num %s de %s" %(self.id, self.tema)


