from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('contact/',views.contact,name='contact'),
    path('destination/',views.destination, name='destination'),
    path('services/',views.services,name='services'),
     path('listings/', views.listing_list, name='listing_list'),
    path('create/', views.listing_create, name='listing_create'),
    path('my-listings/', views.my_listings, name='my_listings'),
    path('listings/<slug:slug>/', views.listing_detail, name='listing_detail'),
    path('listings/<slug:slug>/edit/', views.listing_update, name='listing_update'),
    path('listings/<slug:slug>/delete/', views.listing_delete, name='listing_delete'),
]
