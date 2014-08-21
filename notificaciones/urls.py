from django.conf.urls import patterns, url

from notificaciones import views

urlpatterns = patterns('',

                       url(r'^marcar_leidas/$',
                           views.marcar_leidas, name='marcar_leidas'),
                       url(r'^marcar_leida_redirect/(?P<slug>[-\w]+)/(?P<object_id>\d+)/$',
                           views.marcar_leida_redirect, name='marcar_leida_redirect'),
                       url(r'^index/$',
                           views.notificaciones_index, name='index'),
                       )
