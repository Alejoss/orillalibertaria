from django.conf.urls import patterns, url

from perfiles import views

urlpatterns = patterns('',
                       # urls de editar perfil.
                       url(r'^editar_perfil_des/$', views.editar_perfil_des,
                           name='editar_perfil_des'),
                       url(r'^revisar_nickname/$', views.revisar_nickname,  # Ajax
                           name='revisar_nickname'),
                       # urls de login
                       url(r'^login/$', views.login_page, name="login"),
                       url(r'^authcheck/$', views.authcheck, name="authcheck"),
                       url(r'^logout/$', views.logout, name="logout"),
                       # urls de registro
                       # url(r'^registrar/$', views.registrar, name='registrar'),  # Sin uso por ahora
                       url(r'^(?P<username>[-\w.]+)/postsfav/$', views.postsfav, name='postsfav'),
                       url(r'^(?P<username>[-\w.]+)/(?P<queryset>\w+)/$',
                           views.perfil, name='perfil'),
                       url(r'^allyoutouch/$', views.allyoutouch, name="allyoutouch")
                       )
