from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('trip/<int:pk>/', views.trip_view, name='trip_view'),
    path('user/<int:pk>/', views.user_view, name='user_view'),
    path('admin/upload/', views.admin_upload, name='admin_upload'),
    path('admin/process/', views.admin_process, name='admin_process'),
    path('api/trip', views.trip_list),
    path('api/trip/<int:pk>/', views.trip_detail),
    path('api/trip/<int:pk>/photo', views.photo_list),
    path('api/trip/<int:trip_pk>/upload/<slug:filename>', views.photo_upload),
]
