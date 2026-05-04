
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Listing, AssetType, Category, ListingType
from .forms import ListingForm

# Create your views here.
def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def blog(request):
    return render ( request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def destination(request):
    return render(request,'destinations.html')

def services(request):
    return render(request,'services.html')
# listings/views.py




def listing_list(request):
    """Comprehensive listing view with all filters"""
    
    # Start with available listings
    listings = Listing.objects.filter(is_available=True, is_approved=True)
    
    # Advanced filtering (✅ WHERE YOUR FILTER CODE GOES)
    asset_type = request.GET.get('asset_type')
    if asset_type:
        listings = listings.filter(asset_type__slug=asset_type)
    
    category = request.GET.get('category')
    if category:
        listings = listings.filter(category__slug=category)
    
    listing_type = request.GET.get('listing_type')
    if listing_type:
        listings = listings.filter(listing_type__slug=listing_type)
    
    # Price range filtering
    min_price = request.GET.get('min_price')
    if min_price:
        listings = listings.filter(price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        listings = listings.filter(price__lte=max_price)
    
    # ✅ EXAMPLE: Show special deals (SUVs under $100 for rent)
    special_deals = Listing.objects.filter(
        asset_type__slug='car',
        category__slug='suv',
        listing_type__slug='rent',
        price__lte=100,
        is_available=True
    )[:6]  # Limit to 6
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        listings = listings.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(listings, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filter display
    categories = Category.objects.all()
    asset_types = AssetType.objects.all()
    listing_types = ListingType.objects.all()
    
    context = {
        'listings': page_obj,
        'special_deals': special_deals,  # ✅ Your filtered example
        'categories': categories,
        'asset_types': asset_types,
        'listing_types': listing_types,
        'search_query': search_query,
        'current_asset_type': asset_type,
        'current_category': category,
        'current_listing_type': listing_type,
    }
    
    return render(request, 'main/listing_list.html', context)


def listing_detail(request, slug):
    """Display single listing details"""
    listing = get_object_or_404(Listing, slug=slug, is_available=True)
    
    # Increment view count
    listing.views_count += 1
    listing.save()
    
    # Get related listings
    related_listings = Listing.objects.filter(
        category=listing.category,
        is_available=True
    ).exclude(id=listing.id)[:4]
    
    context = {
        'listing': listing,
        'related_listings': related_listings,
    }
    
    return render(request, 'main/listing_detail.html', context)


@login_required
def listing_create(request):
    """Create new listing through form"""
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            
            # ✅ Create example using form data
            # This is where your CREATE code would be used
            messages.success(request, 'Your listing has been created!')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm()
    
    return render(request, 'main/listing_form.html', {'form': form, 'is_update': False})

@login_required
def my_listings(request):
    """Display user's listings"""
    listings = Listing.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'main/my_listings.html', {'listings': listings})

@login_required
def listing_update(request, slug):
    """Update existing listing"""
    listing = get_object_or_404(Listing, slug=slug, user=request.user)
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your listing has been updated!')
            return redirect('listing_detail', slug=listing.slug)
    else:
        form = ListingForm(instance=listing)
    return render(request, 'main/listing_form.html', {'form': form, 'is_update': True, 'listing': listing})

@login_required
def listing_delete(request, slug):
    """Delete a listing"""
    listing = get_object_or_404(Listing, slug=slug, user=request.user)
    if request.method == 'POST':
        listing.delete()
        messages.success(request, 'Listing has been deleted successfully.')
        return redirect('my_listings')
    return render(request, 'main/listing_confirm_delete.html', {'listing': listing})