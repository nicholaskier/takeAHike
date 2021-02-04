from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.




class Hike(models.Model):
    title = models.CharField(max_length=100)
    summary = models.CharField(max_length=200)
    distance = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('detail', kwargs={'hike_id': self.id})

class Photo(models.Model):
    url = models.CharField(max_length=200)
    hike = models.ForeignKey(Hike, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for hike_id: {self.hike_id} @ {self.url}"