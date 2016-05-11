from django.db import models

class Tweet(models.Model):

    id_str = models.CharField(max_length=255, blank=False, primary_key=True)
    text = models.CharField(max_length=150, blank=False)
    created_at = models.DateTimeField(blank=False)

    coordinates_lon = models.FloatField()
    coordinates_lat = models.FloatField()
    coordinates_type = models.CharField(max_length=255)

    entities_media_id_str = models.CharField(max_length=255)
    entities_media_media_url = models.CharField(max_length=2048)
    entities_media_media_url_https = models.CharField(max_length=2048)
    entities_media_url = models.CharField(max_length=2048)
    entities_media_display_url = models.CharField(max_length=2048)
    entities_media_expanded_url = models.CharField(max_length=2048)
    entities_media_sizes_w = models.IntegerField(null=True)
    entities_media_sizes_h = models.IntegerField(null=True)
    entities_media_sizes_resize = models.CharField(max_length=64)
    entities_media_type = models.CharField(max_length=64)
    entities_media_indices = models.IntegerField(null=True)

    entities_urls_url = models.CharField(max_length=2048)
    entities_urls_display_url = models.CharField(max_length=2048)
    entities_urls_expanded_url = models.CharField(max_length=2048)
    entities_urls_indices = models.IntegerField(null=True)

    entities_user_mentions_id_str = models.CharField(max_length=2048)
    entities_user_mentions_screen_name = models.CharField(max_length=2048)
    entities_user_mentions_name = models.CharField(max_length=2048)
    entities_user_mentions_indices = models.IntegerField(null=True)

    entities_hastags_text = models.CharField(max_length=255)
    entities_hastags_indices = models.IntegerField(null=True)

    entities_symbols_text = models.CharField(max_length=255)
    entities_symbols_indices = models.IntegerField(null=True)

    favorite_count = models.IntegerField(null=True)
    filter_level = models.CharField(max_length=255)

    lang = models.CharField(max_length=4)

    place_attibutes_street_address = models.CharField(max_length=2048)
    place_attibutes_locality = models.CharField(max_length=2048)
    place_attibutes_region = models.CharField(max_length=2048)
    place_attibutes_iso3 = models.CharField(max_length=2048)
    place_attibutes_postal_code = models.CharField(max_length=2048)
    place_attibutes_phone = models.CharField(max_length=2048)
    place_attibutes_twitter = models.CharField(max_length=2048)
    place_attibutes_url = models.CharField(max_length=2048)
    place_attibutes_app_id = models.CharField(max_length=2048)

    place_bounding_box = models.CharField(max_length=2048)
    place_country = models.CharField(max_length=2048)
    place_country_code = models.CharField(max_length=2048)
    place_full_name = models.CharField(max_length=2048)
    place_id = models.CharField(max_length=2048)
    place_name = models.CharField(max_length=2048)
    place_place_type = models.CharField(max_length=2048)
    place_url = models.CharField(max_length=2048)

    class Meta:
        app_label = 'datastore'

    def __str__(self):
        return self.text


class TwitterRouter(object):
    """
    A router to send any data harvested from twitter to the
    "geonode_data" datastore
    """
    def db_for_read(self, model, **hints):
        """
        All attempts to read twitter models go to datastore.
        """
        if model._meta.app_label == 'datastore':
            return 'datastore'
        return None

    def db_for_write(self, model, **hints):
        """
        All attempts to write twitter models go to datastore.
        """
        if model._meta.app_label == 'datastore':
            return 'datastore'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the twitter app is involved.
        """
        if obj1._meta.app_label == 'datastore' or \
           obj2._meta.app_label == 'datastore':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the twitter app only appears in the 'datastore'
        database.
        """
        if db == 'datastore':
            return model._meta.app_label == 'datastore'
        elif model._meta.app_label == 'datastore':
            return False
        return None