from django.conf.urls import patterns, url

from perfiles import views

urlpatterns = patterns('',
                       url(r'^index/$', views.index, name='index'),
                       # urls de editar perfil.
                       url(r'^editar_perfil_des/$', views.editar_perfil_des,
                           name='editar_perfil_des'),
                       url(r'^revisar_nickname/$', views.revisar_nickname,
                           name='revisar_nickname'),
                       # urls de login
                       url(r'^login/$', views.login_page, name="login"),
                       url(r'^authcheck/$', views.authcheck, name="authcheck"),
                       url(r'^logout/$', views.logout, name="logout"),
                       # urls de registro
                       url(r'^registrar/$', views.registrar, name='registrar'),
                       url(r'^registro_ok/$', views.registro_ok,
                           name='registro_ok'),
                       # urls de perfil. perfil/ pasa un string "username" y un queryset
                       url(r'^(?P<username>\w+)/(?P<queryset>\w+)/$',
                           views.perfil, name='perfil'),
                       )
