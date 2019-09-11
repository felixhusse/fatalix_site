from django.db import models
from django.conf import settings
from django.utils import timezone

class ButtonConfiguration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buttonsecret = models.CharField(max_length=50)
    webhookurl = models.CharField(max_length=50)
    webhookoffurl = models.CharField(max_length=50)

    def publish(self):
        self.save()

    def __str__(self):
        return self.title
