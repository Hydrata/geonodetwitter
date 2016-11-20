## geonode-twitter
This app will listen to a specific set of hashtags on twitter and save any georeferenced tweets to a geonode layer

###Installation
1. Open a terminal and navigate into the parent of your geonode folder (usually `/usr/local/lib/python2.7/dist-packages` for geonode 2.4 installed with apt-get)
2. `Git clone https://github.com/Hydrata/geonodetwitter.git`
3. add `"geonodetwitter",` to your `INSTALLED_APPS` in settings.py
4. add `DATABASE_ROUTERS = ['geonodetwitter.models.TwitterRouter']` in settings.py
5. Open a terminal and navigate to your Django root directory (the one with "manage.py" in it)
6. run `python manage.py syncdb --database=datastore`

###Running (this can be replaced with a web interface once we understand how this tool will be used)
1. Open a terminal and navigate to your Django root directory (the one with "manage.py" in it)
2. Run `python manage.py listen examplehastaghere`
3. The captured tweets will be stored in the POSTGIS database, in a table called `geonodetwitter_tweet`
4. CTRL-C to stop lisening

###Viewing (I think this can be replaced with some calls to the geoserver API, but it's a manual job for now)
1. Open the geoserver web interface
2. Select "add layers"
3. Select geonode:datastore
4. Publish "geonodetwitter_tweet"
5. Calculate the min/max bounds 
6. Save
7. Run `python manage.py updatelayers -f geonodetwitter_tweet` from your geonode commandprompt
