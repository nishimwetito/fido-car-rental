from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def blog(request):
    return render ( request,'blog.html')

def booking(request):
    return render(request,'booking.html')

def contact(request):
    return render(request,'contact.html')

def destination(request):
    return render(request,'destinations.html')

def fleet(request):
    return render(request,'fleet.html')

def services(request):
    return render(request,'services.html')