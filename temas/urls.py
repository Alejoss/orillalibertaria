from django.conf.urls import patterns, url
 
from temas import views
 
urlpatterns = patterns('',
	url(r'^$', views.main, name = 'main'),
	url(r'^nuevo_tema/$', views.nuevo_tema, name = 'nuevo_tema'),
	url(r'^buscar/$', views.buscar, name = 'buscar'),
	url(r'^(?P<tema>\w+)/editar_tema/$', views.editar_tema, name = 'editar_tema'),
	url(r'^(?P<titulo>\w+)/$', views.index_tema, name = 'index_tema'),
	url(r'^(?P<tema>\w+)/sumar_post/$', views.sumar_post, name = 'sumar_post'),
	url(r'^(?P<tema>\w+)/nuevo_post/$', views.nuevo_post, name = 'nuevo_post'),
	url(r'^(?P<tema>\w+)/post/(?P<post_id>\d+)/$', views.post, name = 'post'),
	url(r'^(?P<tema>\w+)/post/(?P<post_id>\d+)/respuesta$', 
		views.respuesta, name = 'respuesta'),
	url(r'^(?P<tema>\w+)/(?P<post_id>\d+)/voto$', views.voto, name = 'voto'),
	#prueba
	url(r'^pruebapag/$', views.pruebapag, name = 'pruebapag'),
	)  