from django.db import models
from django.conf import settings
from django.utils import timezone
from taggit.managers import TaggableManager

def path_raw(instance, filename):
    return 'fatalgram/user_{id}/raw/{filename}'.format(id=instance.author.username, filename=filename)

def path_thumb(instance, filename):
    return 'fatalgram/user_{0}/thumbs/{1}'.format(instance.author.username, filename)

class Trip(models.Model):
    title = models.CharField(max_length=50)
    trip_start = models.DateField(blank=True, null=True)
    trip_end = models.DateField(blank=True, null=True)
    summary = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

# Create your models here.
class Photo(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    photo_taken = models.DateTimeField(blank=True, null=True)
    photo_camera = models.CharField(max_length=200, null=True)
    photo_lat = models.CharField(max_length=200, null=True)
    photo_lon = models.CharField(max_length=200, null=True)
    photo_alt = models.CharField(max_length=200, null=True)
    photo_raw = models.ImageField(upload_to=path_raw)
    photo_thumb = models.ImageField(upload_to=path_thumb)
    upload_date = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()

    def publish(self):
        self.save()

    def __str__(self):
        return self.description
