from django.conf.urls import patterns, url

from temas import views

urlpatterns = patterns('',
                       # inicio
                       url(r'^inicio/$', views.inicio, name='inicio'),

                       # aviso legal
                       url(r'^legal/$', views.aviso_legal, name='aviso_legal'),

                       # main page
                       url(r'^index/(?P<queryset>\w+)/$',
                           views.main, name='main'),

                       # Helpers temas
                       url(r'^nuevo_tema/$', views.nuevo_tema,
                           name='nuevo_tema'),
                       url(r'^buscar/$', views.buscar, name='buscar'),
                       url(r'^(?P<slug>[-\w]+)/editar_tema/$',
                           views.editar_tema, name='editar_tema'),

                       # Tema
                       url(r'^(?P<slug>[-\w]+)/(?P<queryset>\w+)/$',
                           views.index_tema, name='index_tema'),

                       # Post
                       url(r'^(?P<slug>[-\w]+)/post/(?P<post_id>\d+)/respuesta/$',
                           views.respuesta, name='respuesta'),
                       url(r'^(?P<slug>[-\w]+)/post/(?P<post_id>\d+)/(?P<queryset>\w+)/$',
                           views.post, name='post'),

                       # Acciones
                       url(r'^/editar_post/(?P<post_id>\d+)/$',
                           views.editar_post, name='editar_post'),
                       url(r'^/sumar_post/(?P<slug>[-\w]+)/$',
                           views.sumar_post, name='sumar_post'),
                       url(r'^/eliminar_post/(?P<post_id>\d+)/$',
                           views.eliminar_propio_post, name='eliminar_propio_post'),
                       # Ajax
                       url(r'^vote_up_ajax/$', views.vote_up_ajax,
                           name='vote_up_ajax'),
                       url(r'^vote_down_ajax/$', views.vote_down_ajax,
                           name='vote_down_ajax'),
                       url(r'^remover_voto_ajax/$', views.remover_voto_ajax,
                           name='remover_voto_ajax'),

                       )
