from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from . forms import RegisterForm
from .models import Profile


# Create your views here.
# REGISTER
def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save( commit= False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User created successfully!')
            login(request,user)
            return redirect('profile')
            
        
    else:
        messages.error(request, 'Registration failed')
        form = RegisterForm()

    context = {'register_form':form}

    return render (request, 'index.html',context)


def login_view(request):
#    if request.user.is_authenticated:
#        return redirect('dashboard')

   if request.method == 'POST':
       username = request.POST.get('username')
       password = request.POST.get('password')

       user = authenticate(request, username=username, password=password)

       if user is not None:
           login(request, user)
           messages.success(request, f'Welcome {user.username}')
           return redirect('profile')
       else:
           messages.error(request, 'Invalid username or password')

   return redirect('index')


# LOGOUT
def logout_view(request):
   logout(request)
   messages.success(request,'Successfully logged out')
   return redirect('login')

# USER PROFILE

@login_required
def profile_view(request):
    """
    Display user profile page
    """
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """
    Handle profile editing via modal form
    """
    if request.method == 'POST':
        # Get the current user and profile
        user = request.user
        profile = user.profile
        
        # Update User model fields
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Check if username is taken (exclude current user)
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
            return redirect('profile')
        
        # Update user fields
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Update Profile model fields
        profile.gender = request.POST.get('gender')
        profile.marital_status = request.POST.get('marital_status')
        profile.phone_number = request.POST.get('phone_number')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            from datetime import datetime
            profile.date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        
        profile.address = request.POST.get('address')
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('profile')
    
    return redirect('profile')




@login_required
def all_profiles(request):
    """
    Display all registered user profiles with search and filter
    """
    # Get all profiles
    profiles_list = Profile.objects.select_related('user').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        profiles_list = profiles_list.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Filter by gender
    gender_filter = request.GET.get('gender', '')
    if gender_filter:
        profiles_list = profiles_list.filter(gender=gender_filter)
    
    # Pagination (12 profiles per page)
    paginator = Paginator(profiles_list, 12)
    page_number = request.GET.get('page')
    profiles = paginator.get_page(page_number)
    
    context = {
        'profiles': profiles,
        'total_members': Profile.objects.count(),
        'search_query': search_query,
        'gender_filter': gender_filter,
    }
    return render(request, 'users/all_profiles.html', context)


@login_required
def profile_detail(request, username):
    """
    Display detailed profile of a specific user
    """
    profile = get_object_or_404(Profile, user__username=username)
    
    context = {
        'viewed_profile': profile,
    }
    return render(request, 'users/profile_details.html', context)



