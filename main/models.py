# models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class AssetType(models.Model):
    """Main classification: Car or Property"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font Awesome icon class")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Specific categories like House, Land, SUV, Economy, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name='categories')
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['asset_type', 'name']
        unique_together = ['name', 'asset_type']
    
    def __str__(self):
        return f"{self.asset_type.name} - {self.name}"


class ListingType(models.Model):
    """Rent or Sale"""
    name = models.CharField(max_length=20, unique=True)  # rent, sale
    slug = models.SlugField(unique=True)
    is_bookable = models.BooleanField(default=False)  # Only rent items are bookable
    description = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Listing(models.Model):
    """Main listing model for both cars and properties"""
    
    # Basic Information
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    # Classification (The Core)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name='listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='listings')
    listing_type = models.ForeignKey(ListingType, on_delete=models.CASCADE, related_name='listings')
    
    # Location
    location = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Images
    main_image = models.ImageField(upload_to='listings/', blank=True, null=True)
    
    # Status
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)  # Admin approval for listings
    
    # User Relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Stats
    views_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset_type', 'listing_type']),
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['location']),
            models.Index(fields=['price']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.listing_type.name}"
    
    def is_bookable(self):
        """Check if this listing can be booked"""
        return self.listing_type.is_bookable and self.is_available
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('listing_detail', kwargs={'slug': self.slug})


class CarDetail(models.Model):
    """Specific fields for car listings"""
    
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    
    FUEL_CHOICES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='car_detail')
    
    # Car Specifications
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2025)])
    seats = models.PositiveIntegerField(default=5)
    doors = models.PositiveIntegerField(default=4)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    mileage = models.PositiveIntegerField(help_text="Current mileage in km", null=True, blank=True)
    
    # Features (Many-to-Many)
    features = models.ManyToManyField('CarFeature', blank=True)
    
    def __str__(self):
        return f"{self.make} {self.model} ({self.year})"


class PropertyDetail(models.Model):
    """Specific fields for property listings"""
    
    PROPERTY_STATUS = [
        ('new', 'New Construction'),
        ('existing', 'Existing'),
        ('under_construction', 'Under Construction'),
    ]
    
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE, related_name='property_detail')
    
    # Property Specifications
    bedrooms = models.PositiveIntegerField(null=True, blank=True)
    bathrooms = models.PositiveIntegerField(null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in square meters", null=True, blank=True)
    land_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Land size in acres or sqm", null=True, blank=True)
    
    # For houses/apartments
    floors = models.PositiveIntegerField(null=True, blank=True)
    parking_spaces = models.PositiveIntegerField(default=0)
    year_built = models.IntegerField(null=True, blank=True)
    property_status = models.CharField(max_length=30, choices=PROPERTY_STATUS, default='existing')
    
    # Features
    features = models.ManyToManyField('PropertyFeature', blank=True)
    
    def __str__(self):
        return f"{self.listing.title} - {self.bedrooms} bed, {self.bathrooms} bath"


class CarFeature(models.Model):
    """Features for cars like A/C, GPS, etc."""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class PropertyFeature(models.Model):
    """Features for properties like pool, garden, etc."""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.name


class ListingImage(models.Model):
    """Multiple images per listing"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.listing.title}"





class Wishlist(models.Model):
    """User wishlist for favorite listings"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'listing']
    
    def __str__(self):
        return f"{self.user.username} - {self.listing.title}"


class ListingReview(models.Model):
    """Reviews for listings"""
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['listing', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.listing.title} ({self.rating} stars)"