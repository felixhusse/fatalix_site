from django import forms
from .models import Photo, Trip
from datetime import datetime
from PIL import Image, ExifTags
from GPSPhoto import gpsphoto

class AdminTripPhotoForm(forms.Form):
    trip_title = forms.CharField(label='Trip Title', max_length=255)
    trip_date = forms.DateField(label='Trip Start',)
    trip_end = forms.DateField(label='Trip End',)
    trip_summary = forms.CharField(label='Trip Summary', widget=forms.Textarea)
    photo_folder = forms.CharField(label='Photo Folder', max_length=255)
