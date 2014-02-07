from django.conf.urls import patterns, url, include
from django.contrib import admin
from core import views

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^challenge/(?P<pk>\d+)/$', views.ChallengeView.as_view(),
        name='challenge-details', ),
    url(r'^user/(?P<pk>\d+)/$', views.PersonView.as_view(),
        name='user-details'),
    # url(r'^facebook-view/(?P<pk>\d+)/$', views.FacebookView.as_view(),
    #     name='facebook-view'),
    url(r'^create-a-challenge/$', views.CreateChallenge.as_view(),
        name='create-a-challenge'),
    url(r'^view-all-challenges/(?P<pk>\d+)/$', views.AllChallenges.as_view(),
        name='view-all-challenges'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    #url(r'^', include('core.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
)