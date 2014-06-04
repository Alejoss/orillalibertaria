from django.conf.urls import patterns, url

from notificaciones import views

urlpatterns = patterns('',

                       url(r'^marcar_leidas/$',
                           views.marcar_leidas, name='marcar_leidas'),
                       url(r'^index/$',
                           views.notificaciones_index, name='index'),
                       )
