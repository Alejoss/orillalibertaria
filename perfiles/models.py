from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Perfiles(models.Model):
    usuario = models.OneToOneField(User, null=True)
    nickname = models.CharField(max_length=75, unique=True, null=True)
    imagen_perfil = models.CharField(max_length=255, null=True)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    votos_recibidos = models.SmallIntegerField(default=0)
    numero_de_posts = models.SmallIntegerField(default=0)
    link1 = models.CharField(max_length=200, blank=True, null=True)
    link2 = models.CharField(max_length=200, blank=True, null=True)
    link3 = models.CharField(max_length=200, blank=True, null=True)
    link4 = models.CharField(max_length=200, blank=True, null=True)
    link5 = models.CharField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        # asegurarse que el usuario no tenga puntaje negativo
        if self.votos_recibidos < 1:
            self.votos_recibidos = 1
        super(Perfiles, self).save(*args, **kwargs)

    def obtener_descripcion(self):
        if self.descripcion is None:
            return ""
        else:
            return self.descripcion

    def __unicode__(self):
        return "perfil de %s" % (self.usuario.username)
