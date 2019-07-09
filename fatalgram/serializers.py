from rest_framework import serializers
from fatalgram.models import Trip, Photo

class TripSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Trip
        fields = ('id', 'title', 'summary', 'trip_start', 'trip_end', 'photo_set')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('id','author','trip','description', 'photo_taken',
                'photo_camera', 'photo_lat', 'photo_lon', 'photo_alt',
                'photo_raw', 'photo_thumb', 'upload_date')
