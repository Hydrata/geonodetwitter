from django.core.management.base import BaseCommand, CommandError
from geonodetwitter.models import Tweet, TwitterRouter
import tweepy, json
from tweepy import OAuthHandler
from geonodetwitter.models import Tweet
from dateutil import parser
from django.contrib.gis.geos import GEOSGeometry
import chennaign.settings as settings


class Command(BaseCommand):
    args = '<hashtag...>'
    help = 'Listens to the twitter.com streaming API for a desired #hashtag'

    def handle(self, *args, **options):

        auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
        auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
        api = tweepy.API(auth)

        for hashtag in args:
            try:
                # Get a list of tweets and convert them to json so we can parse the geo-enabled ones
                tweets = []
                count = 0
                for tweet in tweepy.Cursor(api.search,  q='#%s' % hashtag).items(1000):
                    count += 1
                    tweets.append(json.dumps(tweet._json, indent=2, sort_keys=True))

                # Create an empty GeoJSON file to store our tweets
                geo_tweets = {
                    "type": "FeatureCollection",
                    "features": []
                }

                # parse each tweet to see if it has a 'coordinate' attribute. If it does, then add it to geo_tweets
                for line in tweets:
                    tweet = json.loads(line)
                    if tweet['coordinates']:

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
                        geo_tweets['features'].append(geo_json_feature)

                        # write to models for geonode map
                        temp_point = 'POINT(%s %s)' % (tweet['coordinates'].get('coordinates')[0],
                                                       tweet['coordinates'].get('coordinates')[1]
                                                       )
                        try:
                            Tweet.objects.create(
                                id_str=tweet['id_str'],
                                text=tweet['text'],
                                created_at=parser.parse(tweet['created_at']),
                                coordinates_lon=tweet['coordinates'].get('coordinates')[0],
                                coordinates_lat=tweet['coordinates'].get('coordinates')[1],
                                point=GEOSGeometry(temp_point)

                                # coordinates_type = tweet['id_str'],

                                # entities_media_id_str = tweet['id_str'],
                                # media_url = tweet['media']['media_url']
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
                            error = True

                geo_tweets = json.dumps(geo_tweets, indent=2)

            except error:
                raise CommandError('Something went wrong :( ' % hashtag)
            #
            # poll.opened = False
            # poll.save()

            self.stdout.write('Successfully listened for "%s"' % hashtag)
