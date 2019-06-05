from django.conf import settings
from django.db import models
from django.utils import timezone
from thumbnail_maker.fields import ImageWithThumbnailsField


class Trip(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.TextField(default="no summary")
    trip_date = models.DateField(blank=True, null=True)
    trip_end = models.DateField(blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

class Photo(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=False )
    title = models.CharField(max_length=200)
    photo_taken = models.DateTimeField(blank=True, null=True)
    photo_camera = models.CharField(max_length=200, default="NONE")
    photo_lat = models.CharField(max_length=200, default="NONE")
    photo_lon = models.CharField(max_length=200, default="NONE")
    photo_alt = models.CharField(max_length=200, default="None")
    photo = ImageWithThumbnailsField(upload_to='images/',default='path/to/my/default/image.jpg',thumbs=('photo_small'),)
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
