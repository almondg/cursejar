from django.conf.urls import patterns, include, url
from django.contrib import admin
from cursejar.core import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cursejar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.login, name='login'),
)
