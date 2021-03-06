from django.db import models
from perfiles.models import Perfiles


class Imagen(models.Model):
    url = models.CharField(max_length=250, null=True)
    favoritos_recibidos = models.SmallIntegerField(default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    denunciada = models.SmallIntegerField(default=0)
    eliminada = models.BooleanField(default=False)
    perfil = models.ForeignKey(Perfiles, null=True)
    removidatotalmente = models.BooleanField(default=False)

    def __unicode__(self):
        return "imagen %s_%s" % (self.id, str(self.fecha))


class Ifavoritas(models.Model):
    imagen = models.ForeignKey(Imagen, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    eliminado = models.BooleanField(default=False)
    portada = models.BooleanField(default=False)

    def __unicode__(self):
        return "Ifavoritas obj. %s - %s" % (self.perfil.usuario.username, self.imagen.id)


class Idenunciadas(models.Model):
    imagen = models.ForeignKey(Imagen, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    eliminado = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s denuncio %s" % (self.perfil.usuario.username, self.imagen.id)
