from django.conf.urls import patterns, url
   
from imagenes import views
 
urlpatterns = patterns('',
	url(r'^$', views.index, name = 'index'),
	url(r'^populares/$', views.populares, name = 'populares'),
	url(r'^nueva/$', views.nueva, name = 'nueva'),
	url(r'^(?P<username>\w+)/favoritas/$', views.favoritas, name = 'favoritas'),
	url(r'^marcar_favorito/(?P<imagen_id>\d+)/$', views.marcar_favorito, name = 'marcar_favorito'),
	url(r'^marcar_portada/(?P<imagen_id>\d+)/$', views.marcar_portada, name = 'marcar_portada'),
	url(r'^denunciar/(?P<imagen_id>\d+)/$', views.denunciar, name = 'denunciar'),
	url(r'colaborar_organizar/$', views.colaborar_organizar, name = 'colaborar_organizar'),
	url(r'marcar_visto/(?P<imagen_id>\d+)/$', views.marcar_visto, name = 'marcar_visto'),
	url(r'marcar_x/(?P<imagen_id>\d+)/$', views.marcar_x, name = 'marcar_x'),
	)