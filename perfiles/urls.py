from django.conf.urls import patterns, url

from perfiles import views

urlpatterns = patterns('',
                       url(r'^index/$', views.index, name='index'),
                       # urls de editar perfil.
                       url(r'^editar_perfil_info/$', views.editar_perfil_info,
                           name='editar_perfil_info'),
                       url(r'^editar_perfil_des/$', views.editar_perfil_des,
                           name='editar_perfil_des'),
                       # urls de login
                       url(r'^login/$', views.login_page, name="login"),
                       url(r'^authcheck/$', views.authcheck, name="authcheck"),
                       url(r'^logout/$', views.logout, name="logout"),
                       url(r'^loggedin/$', views.loggedin, name="loggedin"),
                       url(r'^invalid/$', views.invalid, name="invalid"),
                       # urls de registro
                       url(r'^registrar/$', views.registrar, name='registrar'),
                       url(r'^registro_ok/$', views.registro_ok,
                           name='registro_ok'),
                       # urls de perfil. perfil/ pasa un string "username" a la
                       # view function
                       url(r'^(?P<username>\w+)/(?P<queryset>\w+)/$',
                           views.perfil, name='perfil'),
                       )
