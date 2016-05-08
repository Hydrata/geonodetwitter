from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import tweepy, json
from tweepy import OAuthHandler
from models import Tweet

auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

api = tweepy.API(auth)

#
# def tweet_function(self):
#
#     return tweets, geo_tweets


def index(request):

    context = {
        }
    return render(request, 'twitter/twitter_index.html', context)


def json_geo_tweets(request):

    # Get a list of tweets and convert them to json so we can parse the geo-enabled ones
    tweets = []
    count = 0
    for tweet in tweepy.Cursor(api.search,  q='%23flood').items(1000):
        count += 1
        tweets.append(json.dumps(tweet._json, indent=2, sort_keys=True))

    # Create an empty GeoJSON file to store our tweets
    geo_tweets = {
        "type": "FeatureCollection",
        "features": []
    }

    # parse each tweet to see if it has a 'place' attribute. If it does, then add it to geo_tweets
    for line in tweets:
        tweet=json.loads(line)
        if tweet['coordinates']:

            #create json
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                     "text": tweet['text'],
                     "created_at": tweet['created_at'],
                     "id_str": tweet['id_str']
                }

            }
            geo_tweets['features'].append(geo_json_feature)

            #write to models
            Tweet.id_str = tweet['id_str']
            Tweet.text = tweet['text']


    geo_tweets = json.dumps(geo_tweets, indent=2)

    return HttpResponse(geo_tweets, mimetype='application/javascript')
