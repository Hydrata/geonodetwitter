from django.shortcuts import render
from django.http import HttpResponse
from owslib.wps import WebProcessingService

def index(request):
    context = {

    }
    return render(request, 'twitter/twitter_index.html', context)