from django.conf.urls import patterns, url

from citas import views

urlpatterns = patterns('',
                       url(r'^index/(?P<queryset>\w+)/$',
                           views.index, name='index'),

                       url(r'^frase/(?P<cita_id>\d+)/$',
                           views.cita, name='cita'),

                       url(r'nueva/$', views.nueva, name='nueva'),

                       url(r'^(?P<username>[-\w.]+)/favoritas/$',
                           views.favoritas, name='favoritas'),

                       # Ajax
                       url(r'marcar_favorito/$', views.marcar_favorito,
                           name='marcar_favorito'),

                       url(r'denunciar_cita/$', views.denunciar_cita,
                           name='denunciar_cita'),

                       # urls de colaborar_organizar
                       url(r'colaborar_organizar/$', views.colaborar_organizar,
                           name='colaborar_organizar'),
                       url(r'colaborar_organizar/editar/(?P<cita_id>\d+)/$',
                           views.coorg_editar, name='coorg_editar'),
                       url(r'marcar_visto/(?P<cita_id>\d+)/$',
                           views.marcar_visto, name='marcar_visto'),
                       url(r'marcar_x/(?P<cita_id>\d+)/$',
                           views.marcar_x, name='marcar_x'),
                       )
