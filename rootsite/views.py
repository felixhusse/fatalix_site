from django.shortcuts import render
from django.views.generic import ListView

def landing_page(request):
    return render(request, 'rootsite/landing_page.html', {})
