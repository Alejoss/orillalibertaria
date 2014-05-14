from django.conf.urls import patterns, url
from videos import views

urlpatterns = patterns('',
	url(r'^nuevo_video/(?P<slug>[-\w]+)/$', views.nuevo_video, name = 'nuevo_video'),
	url(r'^sumar_post_video/(?P<slug>[-\w]+)/(?P<video_id>\d+)/$', views.sumar_post_video, name = 'sumar_post_video'),
	
	url(r'^(?P<slug>[-\w]+)/(?P<queryset>\w+)/$', views.videos_tema, name = 'videos_tema'),
	url(r'^v/(?P<video_id>\d+)/(?P<slug>[-\w]+)/(?P<queryset>\w+)/$', views.video, name = 'video'),
	url(r'^post_video/(?P<video_id>\d+)/(?P<slug>[-\w]+)/(?P<post_id>\d+)/(?P<queryset>\w+)/$', views.post_video, name = 'post_video'),
	
	url(r'^marcar_favorito/$', views.marcar_favorito, name = 'marcar_favorito'),
	url(r'^denunciar/$', views.denunciar, name = 'denunciar'),
	)
