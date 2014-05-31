from django.db import models
from perfiles.models import Perfiles


class Videos(models.Model):
    tema = models.ForeignKey('temas.Temas', null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    denunciado = models.SmallIntegerField(default=0)
    eliminado = models.BooleanField(default=False)
    favoritos_recibidos = models.SmallIntegerField(default=0)
    titulo = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=1000, null=True)
    url = models.URLField(null=False)
    es_youtube = models.BooleanField(default=True)
    youtube_id = models.CharField(max_length=100, default="")

    def __unicode__(self):
        return "video_id=%s, tema=%s" % (self.id, self.tema.nombre)


class VFavoritos(models.Model):
    video = models.ForeignKey(Videos, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    eliminado = models.BooleanField(default=False)

    def __unicode__(self):
        return "Vfavoritos obj. %s - %s" % (self.perfil.usuario.username, self.video.id)


class VDenunciados(models.Model):
    video = models.ForeignKey(Videos, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    eliminado = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s denuncio %s" % (self.perfil.usuario.username, self.video.id)
