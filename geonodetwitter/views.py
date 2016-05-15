from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core import management
from .models import HashtagStatus
from .forms import HashtagStatusForm


def home(request):

    if request.method == 'POST':
        form = HashtagStatusForm(request.POST)

        if form.is_valid():
            form.cleaned_data['is_listening'] = True
            form.save()
            try:
                HashtagStatus.objects.filter(hashtag=form.cleaned_data['hashtag']).update(is_listening=True)
                management.call_command('listen', form.cleaned_data['hashtag'], interactive=False)
            except:
                error_message = 'Attempt to listen has failed.'

        return redirect('/twitter')

    else:
        form = HashtagStatusForm()

    context = {
        'form': form,
        'hashtag_status': HashtagStatus.objects.all()
        }
    return render(request, 'twitter/twitter_home.html', context)


def json_geo_tweets(request):

    geo_tweets = {
        'test': 'test'
    }

    return HttpResponse(geo_tweets, mimetype='application/javascript')
