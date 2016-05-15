from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^json_geo_tweets/$', views.json_geo_tweets, name='json_geo_tweets')
]