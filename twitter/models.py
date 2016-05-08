from django.db import models

class Tweet(models.Model):

    id_str = models.CharField(max_length=255)
    text = models.CharField(max_length=150)

    #created_at = models.DateTimeField()

    def __str__(self):
        return self.text