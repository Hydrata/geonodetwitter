from django.core.management.base import BaseCommand, CommandError
import tweepy, json
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from dateutil import parser
from django.contrib.gis.geos import GEOSGeometry
import cfm.settings as settings
from apps.geonodetwitter.models import Tweet, TwitterRouter, HashtagStatus
import datetime
import time


def twitterlog(logtext):
    print logtext
    with open("/var/log/geonode/twitterlog.txt", 'a') as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + logtext + "\n")


class MyStreamListener(StreamListener):

    def on_data(self, data):

        tweet = json.loads(data)

        try:
            hashtag = tweet['entities'].get('hashtags')[0].get('text')
        except TypeError:
            hashtag = ""

        try:
            media_url = tweet['entities'].get('media')[0]['media_url']
        except TypeError:
            media_url = ""

        if 'limit' in tweet:
            twitterlog("ERROR - The tweet feed is limited.")

        elif tweet['coordinates']:
            twitterlog("Data with Exact Coordinates : " + str(data))

            # Create the point in GEOSGeometry format
            temp_point = 'POINT(%s %s)' % (tweet['coordinates'].get('coordinates')[0],
                                           tweet['coordinates'].get('coordinates')[1]
                                           )
            # write to models for geonode map
            twitterlog("About to create Tweet - ")

            try:
                Tweet.objects.create(
                    # todo: use a for loop to get all the hashtags, not just first one
                    hashtag=hashtag,
                    id_str=tweet['id_str'],
                    text=tweet['text'].encode('utf-8'),
                    created_at=parser.parse(tweet['created_at']),
                    coordinates_lon=tweet['coordinates'].get('coordinates')[0],
                    coordinates_lat=tweet['coordinates'].get('coordinates')[1],
                    point=GEOSGeometry(temp_point),
                    media_url=media_url,
                    data=data
                )
                twitterlog("That seems to have worked... ")

            except Exception as e:
                twitterlog("Tweet error - " + str(e))

        elif tweet['place']:
            twitterlog("Data with Place : " + str(data))
            try:
                bbox = tweet['place'].get('bounding_box')['coordinates']
                twitterlog("This tweet has a bounding box but no exact location - " + str(bbox))
                x_min = tweet['place'].get('bounding_box')['coordinates'][0][0][0]
                x_max = tweet['place'].get('bounding_box')['coordinates'][0][2][0]
                y_min = tweet['place'].get('bounding_box')['coordinates'][0][0][1]
                y_max = tweet['place'].get('bounding_box')['coordinates'][0][2][1]
                x_spread = x_max - x_min
                y_spread = y_max - y_min
                x_centre = x_min + x_spread/2
                y_centre = y_min + y_spread/2
                radius = max(x_spread, y_spread)/2
                twitterlog(
                    " xmin:" + str(x_min) +
                    " x_max:" + str(x_max) +
                    " x_spread:" + str(x_spread) +
                    " x_centre:" + str(x_centre) +
                    " y_min:" + str(y_min) +
                    " y_max:" + str(y_max) +
                    " y_centre:" + str(y_centre) +
                    " y_spread:" + str(y_spread) +
                    " radius:" + str(radius)
                )
                # Create the point in GEOSGeometry format
                temp_point = 'POINT(%s %s)' % (x_centre, y_centre)
                # write to models for geonode map
                twitterlog("About to create Tweet with bbox  - ")

                try:
                    Tweet.objects.create(
                        # todo: use a for loop to get all the hashtags, not just first one
                        hashtag=hashtag,
                        id_str=tweet['id_str'],
                        text=tweet['text'].encode('utf-8'),
                        created_at=parser.parse(tweet['created_at']),
                        coordinates_lon=x_centre,
                        coordinates_lat=y_centre,
                        point=GEOSGeometry(temp_point),
                        radius=radius,
                        media_url=media_url,
                        data=data
                    )
                    twitterlog("That seems to have worked with bbox ")

                except Exception as e:
                    twitterlog("Tweet error with bbox - " + str(e))

            except Exception as e:
                twitterlog("Tweet error - we have place but no bbox - " + str(e))

        else:
            twitterlog("Passing this tweet by with no coords or bbox - " + str(tweet['text'].encode('utf-8')))

    def on_error(self, status):
        if status == 420:
            twitterlog(str(status) + "=== disconnecting to avoid limiting our stream")
            #returning False in on_data disconnects the stream
            return False

        twitterlog("Oh no, MyStreamListener error!")
        twitterlog(status)
        return True

class Command(BaseCommand):
    args = '<hashtag...>'
    help = 'Listens to the twitter.com streaming API for a desired #hashtag'

    def handle(self, *args, **options):

        #standard tweepy boilerplate
        auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
        api = tweepy.API(auth)

        my_stream = tweepy.Stream(auth=api.auth, listener=MyStreamListener())
        try:
            my_stream.filter(track=[
                '#chennairains',
                '#flood',
                '#flooding',
                '#chennaiflood',
                '#chennaiweather',
            ], async=True)
        except Exception as e:
            twitterlog("my_stream.filter error - " + str(e))
