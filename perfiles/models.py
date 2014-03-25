from django.db import models
from django.template import defaultfilters
from django.contrib.auth.models import User
   
# Create your models here.
class Perfiles(models.Model):
	usuario = models.OneToOneField(User, null = True)
	descripcion = models.CharField(max_length=250, blank=True, null=True)
	votos_recibidos = models.SmallIntegerField(default=0)
	numero_de_posts = models.SmallIntegerField(default=0)
	link1 =models.CharField(max_length=200, blank=True, null=True)
	link2 =models.CharField(max_length=200, blank=True, null=True)
	link3 =models.CharField(max_length=200, blank=True, null=True)
	link4 =models.CharField(max_length=200, blank=True, null=True)
	link5 =models.CharField(max_length=200, blank=True, null=True)
	link6 =models.CharField(max_length=200, blank=True, null=True)
	link7 =models.CharField(max_length=200, blank=True, null=True)
	link8 =models.CharField(max_length=200, blank=True, null=True)
	link9 =models.CharField(max_length=200, blank=True, null=True)
	link10 =models.CharField(max_length=200, blank=True, null=True)

	def __unicode__(self):
		return "perfil de %s" %(self.usuario.username)