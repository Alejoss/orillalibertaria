from django.db import models
from perfiles.models import Perfiles
# Create your models here.


class Cita(models.Model):
    texto = models.CharField(max_length=1000, null=True)
    autor = models.CharField(max_length=75, null=True)
    fuente = models.CharField(max_length=75, null=True)
    favoritos_recibidos = models.SmallIntegerField(default=0)
    creador = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    denunciada = models.SmallIntegerField(default=0)
    correcta = models.BooleanField(default=False)  # Todavia no se usa este campo
    eliminada = models.BooleanField(default=False)
    removidatotalmente = models.BooleanField(default=False)

    #!!!cuando se elimine una cita, eliminar en el modelo CFavoritas

    def __unicode__(self):
        return "%s de %s" % (self.id, self.autor)


class Cfavoritas(models.Model):
    cita = models.ForeignKey(Cita, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    eliminado = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - %s" % (self.perfil.usuario.username, self.cita.autor)


class Ceditadas(models.Model):
    cita = models.ForeignKey(Cita, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    razon = models.CharField(max_length=250, null=True)

    def __unicode__(self):
        return "%s editada el %s" % (self.cita.autor, self.fecha)


class Cdenunciadas(models.Model):
    cita = models.ForeignKey(Cita, null=True)
    perfil = models.ForeignKey(Perfiles, null=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    eliminado = models.BooleanField(default=False)
