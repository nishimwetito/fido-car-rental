from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from main.models import Listing
from decimal import Decimal

@login_required
def create_booking(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_available=True)
    
    if not listing.listing_type.is_bookable:
        messages.error(request, "This listing is not available for booking.")
        return redirect('listing_detail', slug=listing.slug)
        
    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        special_requests = request.POST.get('special_requests', '')
        
        # Simple validation
        if not start_date_str or not end_date_str:
            messages.error(request, "Please provide both start and end dates.")
            return redirect('booking:create', listing_id=listing.id)
            
        try:
            start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('booking:create', listing_id=listing.id)
            
        if start_date < timezone.now().date():
            messages.error(request, "Start date cannot be in the past.")
            return redirect('booking:create', listing_id=listing.id)
            
        if end_date <= start_date:
            messages.error(request, "End date must be after start date.")
            return redirect('booking:create', listing_id=listing.id)
            
        # Check availability
        overlapping_bookings = Booking.objects.filter(
            listing=listing,
            status__in=['pending', 'confirmed'],
            start_date__lte=end_date,
            end_date__gte=start_date
        )
        
        if overlapping_bookings.exists():
            messages.error(request, "These dates are not available.")
            return redirect('booking:create', listing_id=listing.id)
            
        # Calculate price (Days * Price)
        days = (end_date - start_date).days
        total_price = listing.price * Decimal(days)
        
        booking = Booking.objects.create(
            listing=listing,
            user=request.user,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            full_name=full_name,
            email=email,
            phone=phone,
            special_requests=special_requests
        )
        
        messages.success(request, "Booking requested successfully!")
        return redirect('booking:success', booking_id=booking.id)

    context = {
        'listing': listing,
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
def booking_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_success.html', {'booking': booking})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})
