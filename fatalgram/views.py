import os
import tempfile

from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework import generics

from .services import PhotoService
from .models import Photo, Trip
from .tasks import processZipFile, processPhoto
from .serializers import TripSerializer, PhotoSerializer



# Create your views here.

@login_required
def home(request):
    photo_list = Photo.objects.all().order_by('photo_taken').reverse()
    trips = Trip.objects.all().order_by('trip_start').reverse()
    web_trips = []
    for trip in trips:
        if trip.photo_set.count() > 0:
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

    if request.GET.get('delete'):
        photoService = PhotoService()
        photoService.deletePhoto(request.GET.get('delete'))

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
        user_id = request.user.id
        trip_id = request.POST.get('trip_id')
        trip = get_object_or_404(Trip, pk=trip_id)
        photoService = PhotoService()
        result = "processed files:"
        for dirName, subdirList, fileList in os.walk(settings.MEDIA_ROOT + "/fatalgram/temp"):
            for fname in fileList:
                if ".zip" in fname:
                    result = result + ","+fname
                    processZipFile.delay(trip_id=trip_id,photozip=os.path.join(dirName, fname),user_id=user_id)
        return render(request, 'fatalgram/admin/process.html', {"result":result})

    return render(request, 'fatalgram/admin/process.html', {})

@api_view(['GET','POST'])
def trip_list(request):
    if request.method == 'GET':
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET','POST'])
def trip_detail(request, pk):
    try:
        trip = Trip.objects.get(pk=pk)
    except Trip.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TripSerializer(trip)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TripSerializer(trip, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        trip.delete()
        return Response(status=204)

@api_view(['PUT'])
@parser_classes((FileUploadParser,))
def photo_upload(request, trip_pk, filename):
    photoUpload = request.FILES['file']
    filename = settings.MEDIA_ROOT+'/fatalgram/temp/'+photoUpload.name
    with open(filename, 'wb+') as temp_file:
        for chunk in photoUpload.chunks():
            temp_file.write(chunk)
        processPhoto.delay(trip_id=trip_pk,photo_path=filename,user_id=request.user.id)
    return Response(status=204)


@api_view(['GET','POST'])
def photo_list(request,pk):
    if request.method == 'GET':
        trip = get_object_or_404(Trip, pk=pk)
        photo_list = trip.photo_set.all().order_by('photo_taken')
        serializer = PhotoSerializer(photo_list, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PhotoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
