from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about, name='about'),
    path('blog/',views.blog, name='blog'),
    path('booking/',views.booking, name='booking'),
    path('contact/',views.contact,name='contact'),
    path('destination/',views.destination, name='destination'),
    path('fleet/',views.fleet,name='fleet'),
    path('services/',views.services,name='services'),
]
