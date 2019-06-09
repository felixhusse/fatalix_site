from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('trip/<int:pk>/', views.trip_view, name='trip_view'),
    path('admin/upload/', views.admin_upload, name='admin_upload'),
    path('admin/process/', views.admin_process, name='admin_process'),
]
