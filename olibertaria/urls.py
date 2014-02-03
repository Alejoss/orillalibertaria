from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'olibertaria.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^perfiles/', include('perfiles.urls', namespace = 'perfiles')),
    url(r'^temas/', include('temas.urls', namespace = 'temas')),
    url(r'^admin/', include(admin.site.urls)),
)
