# listings/admin.py

from django.contrib import admin
from .models import Listing, AssetType, Category, ListingType

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_type', 'slug']

@admin.register(ListingType)
class ListingTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_bookable']

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'asset_type', 'category', 'listing_type', 'price', 'is_available', 'is_approved']
    list_filter = ['asset_type', 'category', 'listing_type', 'is_available', 'is_approved']
    search_fields = ['title', 'location', 'description']
    list_editable = ['is_available', 'is_approved']