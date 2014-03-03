from django.conf.urls import patterns, url
   
from imagenes import views
 
urlpatterns = patterns('',
	url(r'^$', views.index, name = 'index'),
	url(r'^nueva/$', views.nueva, name = 'nueva'),
	url(r'^prueba/$', views.prueba, name = 'prueba'),
	url(r'^(?P<username>\w+)/favoritas/$', views.favoritas, name = 'favoritas'),
	url(r'^marcar_favorito/(?P<imagen_id>\d+)/$', views.marcar_favorito, name = 'marcar_favorito'),
	url(r'^marcar_portada/(?P<imagen_id>\d+)/$', views.marcar_portada, name = 'marcar_portada'),
	)