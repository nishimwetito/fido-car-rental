from django.db import models
from django.contrib.auth.models import User
from main.models import Listing

class Booking(models.Model):
    """Booking system for rent items only"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking Details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Contact Information (for booking)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    special_requests = models.TextField(blank=True)
    
    # Payment (simplified for now)
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking for {self.listing.title} by {self.user.username}"
    
    def clean(self):
        """Validate that only rent items can be booked"""
        if not self.listing.is_bookable():
            from django.core.exceptions import ValidationError
            raise ValidationError("This listing is not available for booking.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
