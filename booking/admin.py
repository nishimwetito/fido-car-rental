from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'user', 'start_date', 'end_date', 'status', 'is_paid']
    list_filter = ['status', 'is_paid', 'created_at']
    search_fields = ['listing__title', 'user__username', 'full_name', 'email']
    list_editable = ['status', 'is_paid']
    date_hierarchy = 'start_date'
    
    actions = ['mark_as_paid', 'mark_as_confirmed']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
    mark_as_paid.short_description = "Mark selected bookings as paid"
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"
