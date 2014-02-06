from django.conf.urls import patterns, include, url
from django.contrib import admin
from core import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cursejar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^challenge/(?P<pk>\d+)/$', views.ChallengeView.as_view(),
        name='challenge-details',
        kwargs={}),
    url(r'^user/(?P<pk>\d+)/$', views.PersonView.as_view(),
        name='user-details')
)