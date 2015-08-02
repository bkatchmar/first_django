from django.conf.urls import patterns, url
from nhlhockey import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<conference>eastern|western)/$', views.conference, name='conference'),
    url(r'^(?P<conference>eastern|western)/(?P<division>metropolitan|atlantic|central|pacific)/$', views.division, name='division'),
    url(r'^(?P<conference>eastern|western)/(?P<division>metropolitan|atlantic|central|pacific)/(?P<teamname>[a-z-]+)/$', views.team, name='team')
)