from django.conf.urls import patterns, url
 
from temas import views
 
urlpatterns = patterns('',
	# main page
	url(r'^index/(?P<queryset>\w+)/$', views.main, name = 'main'),
	
	# Helpers temas
	url(r'^nuevo_tema/$', views.nuevo_tema, name = 'nuevo_tema'),
	url(r'^buscar/$', views.buscar, name = 'buscar'),
	url(r'^(?P<slug>[-\w]+)/editar_tema/$', views.editar_tema, name = 'editar_tema'),
	
	#Tema
	url(r'^(?P<slug>[-\w]+)/(?P<queryset>\w+)/$', views.index_tema, name = 'index_tema'),

	#Post
	url(r'^(?P<slug>[-\w]+)/post/(?P<post_id>\d+)/$', views.post, name = 'post'),
	url(r'^(?P<slug>[-\w]+)/post/(?P<post_id>\d+)/respuesta/$', 
		views.respuesta, name = 'respuesta'),
	
	#Acciones
	url(r'^/sumar_post/(?P<slug>[-\w]+)/$', views.sumar_post, name = 'sumar_post'),
	url(r'^/eliminar_post/(?P<post_id>\d+)/$', views.eliminar_propio_post, name = 'eliminar_propio_post'),
	url(r'^(?P<slug>[-\w]+)/(?P<post_id>\d+)/voto$', views.voto, name = 'voto'),
	)  