from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView,ListView
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import Trip,Photo
from .forms import AdminTripPhotoForm
from .services import PhotoService, TripService


# Create your views here.
def trip_overview(request):
    trips = Trip.objects.order_by('trip_date')
    return render(request, 'reiseblog/trip_overview.html', {'trips':trips})

def trip_detail(request,pk):
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
    return render(request, 'reiseblog/trip_detail.html', {'photos': photos, 'trip':trip})

@login_required
def admin_tripupload(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = AdminTripPhotoForm(request.POST)
        if form.is_valid():
            # process Trip data
            tripService = TripService()
            photoService = PhotoService()
            trip_title = form.cleaned_data['trip_title']
            trip_date = form.cleaned_data['trip_date']
            trip_end = form.cleaned_data['trip_end']
            trip_summary = form.cleaned_data['trip_summary']
            photo_folder = form.cleaned_data['photo_folder']
            trip = tripService.createTrip(title=trip_title, startDate=trip_date, endDate=trip_end, summary=trip_summary, user=request.user)

            # process folder with photos
            photoService.importFolder(trip=trip, photo_folder=photo_folder)
            return HttpResponseRedirect('/reise/')
    else:
        form = AdminTripPhotoForm()
    return render(request, 'reiseblog/admin_tripupload.html', {'form':form})
