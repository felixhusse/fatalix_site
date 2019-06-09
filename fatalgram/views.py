from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings

from .services import PhotoService
from .models import Photo, Trip

# Create your views here.

@login_required
def home(request):
    photo_list = Photo.objects.all().order_by('photo_taken').reverse()
    trips = Trip.objects.all().order_by('trip_start').reverse()
    web_trips = []
    for trip in trips:
        covers = trip.photo_set.all()[:1]
        web_trip = {'title':trip.title,
                    'trip_start':trip.trip_start,
                    'trip_end':trip.trip_end,
                    'cover':covers[0].photo_thumb.url,
                    'pk':trip.pk}
        web_trips.append(web_trip)


    page = request.GET.get('page', 1)
    paginator = Paginator(photo_list, 8)
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request, 'fatalgram/home.html', {'photos': photos, 'trips':web_trips})

@login_required
def trip_view(request,pk):
    trip = get_object_or_404(Trip, pk=pk)
    photo_list = trip.photo_set.all().order_by('photo_taken')
    page = request.GET.get('page', 1)
    paginator = Paginator(photo_list, 25)
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)
    return render(request, 'fatalgram/trip.html', {'photos': photos, 'trip':trip})

@login_required
def admin_upload(request):
    if request.method == 'POST' and request.FILES['photozip']:
        photozip = request.FILES['photozip']
        trip_id = request.POST.get('trip_id')
        fs = FileSystemStorage()
        filename = fs.save("fatalgram/temp/"+photozip.name, photozip)
        uploaded_file_url = fs.url(filename)
        trip = get_object_or_404(Trip, pk=trip_id)
        photoService = PhotoService()
        result = photoService.processZipFile(trip=trip,photozip=fs.path(filename),user=request.user)
        return render(request, 'fatalgram/admin/upload.html', {'uploaded_file_url': uploaded_file_url, "result":result})

    return render(request, 'fatalgram/admin/upload.html', {})

@login_required
def admin_process(request):
    if request.method == 'POST':
        trip_id = request.POST.get('trip_id')
        trip = get_object_or_404(Trip, pk=trip_id)
        photoService = PhotoService()
        result = photoService.processZipFile(trip=trip,photozip=settings.MEDIA_ROOT + "/fatalgram/temp/archive.zip",user=request.user)
        return render(request, 'fatalgram/admin/process.html', {"result":result})

    return render(request, 'fatalgram/admin/process.html', {})
