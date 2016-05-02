from django.conf.urls import patterns, url
from django.conf import settings
from django.views.generic import TemplateView

from . import views

app_name = 'twitter'

urlpatterns = [
    url(r'^$', views.index, name='index')
]