from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('create/<int:listing_id>/', views.create_booking, name='create'),
    path('success/<int:booking_id>/', views.booking_success, name='success'),
    path('detail/<int:booking_id>/', views.booking_detail, name='detail'),
]
