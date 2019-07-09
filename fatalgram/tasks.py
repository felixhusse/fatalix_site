# Create your tasks here

from __future__ import absolute_import, unicode_literals
import os
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import Trip, Photo
from django.contrib.auth.models import User
from .services import PhotoService


@shared_task
def processZipFile(trip_id, photozip, user_id):
    trip = Trip.objects.get(pk=trip_id)
    user = User.objects.get(pk=user_id)
    photoService = PhotoService()
    return photoService.processZipFile(trip=trip,photozip=photozip,user=user)

@shared_task
def processPhoto(trip_id,photo_path,user_id):
    trip = Trip.objects.get(pk=trip_id)
    user = User.objects.get(pk=user_id)
    photoService = PhotoService()
    return photoService.processPhoto(photo_path=photo_path, trip=trip, user=user)
