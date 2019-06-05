import os
import glob
from django.core.files.images import ImageFile
from django.core.files import File as FileWrapper

from datetime import datetime
from PIL import Image, ExifTags
from GPSPhoto import gpsphoto

from .models import Trip, Photo

class PhotoService():

    def importFolder(self, trip, photo_folder):
        imageFiles = [f for f in glob.glob(photo_folder + "**/*.jpg", recursive=True)]
        for imageFile in imageFiles:
            self.processPhoto(photo_path=imageFile, trip=trip)

    def get_exif(self,url):
        img = Image.open(url)
        exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        return exif

    def processPhoto(self,photo_path, trip):
        exifData = self.get_exif(photo_path)
        gpsData = gpsphoto.getGPSData(photo_path)

        photo = Photo(trip=trip, title=photo_path)
        photo.photo = ImageFile(open(photo_path, "rb"))
        photo.photo_taken = datetime.strptime(exifData['DateTime'], '%Y:%m:%d %H:%M:%S')
        photo.photo_camera = exifData['Model']
        try:
            photo.photo_lat = gpsData['Latitude']
            photo.photo_lon = gpsData['Longitude']
            photo.photo_alt = gpsData['Altitude']
        except:
           # handle all other exceptions
           pass
        photo.save()

class TripService():

    def createTrip(self,title,startDate, endDate, summary, user):
        trip = Trip(author = user, title=title, summary=summary, trip_date=startDate, trip_end=endDate)
        trip.save()
        return trip
