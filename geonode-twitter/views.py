from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import tweepy, json
from tweepy import OAuthHandler
from chennaign.twitter.models import Tweet
from dateutil import parser

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
    for tweet in tweepy.Cursor(api.search,  q='#rain').items(500):
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
            try:
                Tweet.objects.create(
                    id_str=tweet['id_str'],
                    text=tweet['text'],
                    created_at=parser.parse(tweet['created_at']),

                    coordinates_lon = tweet['coordinates'].get('coordinates')[0],
                    coordinates_lat = tweet['coordinates'].get('coordinates')[1]
                    # coordinates_type = tweet['id_str'],

                    # entities_media_id_str = tweet['id_str'],
                    # entities_media_media_url = tweet['id_str'],
                    # entities_media_media_url_https = tweet['id_str'],
                    # entities_media_url = tweet['id_str'],
                    # entities_media_display_url = tweet['id_str'],
                    # entities_media_expanded_url = tweet['id_str'],
                    # entities_media_sizes_w = tweet['id_str'],
                    # entities_media_sizes_h = tweet['id_str'],
                    # entities_media_sizes_resize = tweet['id_str'],
                    # entities_media_type = tweet['id_str'],
                    # entities_media_indices = tweet['id_str'],
                    #
                    # entities_urls_url = tweet['id_str'],
                    # entities_urls_display_url = tweet['id_str'],
                    # entities_urls_expanded_url = tweet['id_str'],
                    # entities_urls_indices = tweet['id_str'],
                    #
                    # entities_user_mentions_id_str = tweet['id_str'],
                    # entities_user_mentions_screen_name = tweet['id_str'],
                    # entities_user_mentions_name = tweet['id_str'],
                    # entities_user_mentions_indices = tweet['id_str'],
                    #
                    # entities_hastags_text = tweet['id_str'],
                    # entities_hastags_indices = tweet['id_str'],
                    #
                    # entities_symbols_text = tweet['id_str'],
                    # entities_symbols_indices = tweet['id_str'],
                    #
                    # favorite_count = tweet['id_str'],
                    # filter_level = tweet['id_str'],
                    #
                    # lang = tweet['id_str'],
                    #
                    # place_attibutes_street_address = tweet['id_str'],
                    # place_attibutes_locality = tweet['id_str'],
                    # place_attibutes_region = tweet['id_str'],
                    # place_attibutes_iso3 = tweet['id_str'],
                    # place_attibutes_postal_code = tweet['id_str'],
                    # place_attibutes_phone = tweet['id_str'],
                    # place_attibutes_twitter = tweet['id_str'],
                    # place_attibutes_url = tweet['id_str'],
                    # place_attibutes_app_id = tweet['id_str'],
                    #
                    # place_bounding_box = tweet['id_str'],
                    # place_country = tweet['id_str'],
                    # place_country_code = tweet['id_str'],
                    # place_full_name = tweet['id_str'],
                    # place_id = tweet['id_str'],
                    # place_name = tweet['id_str'],
                    # place_place_type = tweet['id_str'],
                    # place_url = tweet['id_str']
                )
            except:
                pass


    geo_tweets = json.dumps(geo_tweets, indent=2)

    return HttpResponse(geo_tweets, mimetype='application/javascript')
