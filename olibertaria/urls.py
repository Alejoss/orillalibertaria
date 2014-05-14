from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'olibertaria.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^perfiles/', include('perfiles.urls', namespace = 'perfiles')),
    url(r'^temas/', include('temas.urls', namespace = 'temas')),
    url(r'^citas/', include('citas.urls', namespace = 'citas')),
    url(r'^imagenes/', include('imagenes.urls', namespace = 'imagenes')),
    url(r'^videos/', include('videos.urls', namespace = 'videos')),
    url(r'^admin/', include(admin.site.urls)),
) +static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
