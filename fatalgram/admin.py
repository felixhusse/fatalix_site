from django.contrib import admin

from .models import Trip
from .models import Photo


# Register your models here.
admin.site.register(Trip)
admin.site.register(Photo)
