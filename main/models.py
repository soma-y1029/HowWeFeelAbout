from django.db import models


# Create your models here.
class mainItem(models.Model):
    content = models.TextField()
    result = models.IntegerField(default=50)
    # positive_tweets = models.TextField()
    # negative_tweets = models.TextField()
