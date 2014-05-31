from django.db import models

from perfiles.models import Perfiles
# Create your models here.


class Notificacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    actor = models.ForeignKey(Perfiles, related_name="actor", null=True)
    target = models.ForeignKey(Perfiles, related_name="receptor")
    objeto_id = models.PositiveIntegerField(null=True)
    tipo_objeto = models.CharField(max_length=20, null=True)  # Post, Video, Cita, Imagen
    tipo_notificacion = models.CharField(max_length=20, blank=True, null=True)  # fav_voteup, num, comment, denuncia
    leida = models.BooleanField(default=False)

    def __unicode__(self):
        return "notificacion tipo %s para %s" % (self.tipo_objeto, self.target.usuario.username)
