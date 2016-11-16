from django.conf.urls import url, patterns
from . import views

app_name = 'geonodetwitter'

urlpatterns = patterns(
    '',
    url(r'^$', views.twitter_home, name='twitter_home'),
    url(r'^json_geo_tweets/$', views.json_geo_tweets, name='json_geo_tweets')
)