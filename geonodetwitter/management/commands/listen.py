from django.core.management.base import BaseCommand, CommandError
import tweepy, json
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from dateutil import parser
from django.contrib.gis.geos import GEOSGeometry
import chennaign.settings as settings
from geonodetwitter.models import Tweet, TwitterRouter, HashtagStatus


class MyStreamListener(StreamListener):

    def on_data(self, data):
        #raw_input("PRESS ENTER TO CONTINUE1.")

        tweet = json.loads(data)
        # hashtag = '#chennairains'

        # print(tweet['limit'])
        #print(tweet)
        #raw_input("PRESS ENTER TO CONTINUE2.")

        if 'limit' in tweet:
            #print(data)
            print('This tweet has limit')
            #raw_input("PRESS ENTER TO CONTINUE3.")

        elif tweet['coordinates']:
            #print(data)
            print('This tweet has coordinates')
            #raw_input("PRESS ENTER TO CONTINUE4.")

            # create json for preview map
            geo_json_feature = {
                "type": "Feature",
                "geometry": tweet['coordinates'],
                "properties": {
                     "text": tweet['text'],
                     "created_at": tweet['created_at'],
                     "id_str": tweet['id_str']
                }
            }

            geo_tweets = {
                "type": "FeatureCollection",
                "features": []
                }

            geo_tweets['features'].append(geo_json_feature)

            # Create the point in GEOSGeometry format
            temp_point = 'POINT(%s %s)' % (tweet['coordinates'].get('coordinates')[0],
                                           tweet['coordinates'].get('coordinates')[1]
                                           )
            # write to models for geonode map
            # try:
            Tweet.objects.create(
                #hashtag=hashtag,
                hashtag='varied',
                id_str=tweet['id_str'],
                text=tweet['text'],
                created_at=parser.parse(tweet['created_at']),
                coordinates_lon=tweet['coordinates'].get('coordinates')[0],
                coordinates_lat=tweet['coordinates'].get('coordinates')[1],
                point=GEOSGeometry(temp_point)
            )
        else:
            print("passing this tweet by")
            #raw_input("press enter to continue")
            # except:
            #     error = True

    def on_error(self, status):
        print("Oh no, error!")
        print(status)
        raw_input("Press Enter to continue")
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

        for hashtag in args:
            error = False
            try:
                my_stream.filter(track=['#chennairains', '#tamil nadu', '#chennaiflood', 'chennaiweather'])

            except error:
                raise CommandError('Something went wrong :( %s' % hashtag)

            self.stdout.write('Successfully listened for "%s"' % hashtag)
