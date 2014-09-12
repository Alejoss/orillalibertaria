from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from temas import views

urlpatterns = patterns('',
                       # Python social auth
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       # Redirect a main si accede el usuario a orillalibertaria.com
                       url('', views.inicio, name="inicio_redirect"),
                       url(r'^perfiles/',
                           include('perfiles.urls', namespace='perfiles')),
                       url(r'^temas/',
                           include('temas.urls', namespace='temas')),
                       url(r'^citas/',
                           include('citas.urls', namespace='citas')),
                       url(r'^imagenes/',
                           include('imagenes.urls', namespace='imagenes')),
                       url(r'^videos/',
                           include('videos.urls', namespace='videos')),
                       url(r'^notificaciones/',
                           include('notificaciones.urls', namespace='notificaciones')),
                       ) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
