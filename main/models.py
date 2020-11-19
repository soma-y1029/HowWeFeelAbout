from django.db import models


# Create your models here.
class mainItem(models.Model):
    content = models.CharField(max_length=50)
    result = models.IntegerField(max_length=3)

