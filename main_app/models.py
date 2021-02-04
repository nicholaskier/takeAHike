from django.db import models
from django.urls import reverse
# Create your models here.




class Hike(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    distance = models.IntegerField()

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail', kwargs={'hike_id': self.id})