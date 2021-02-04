from django.db import models

# Create your models here.




class Hike(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    distance = models.IntegerField()