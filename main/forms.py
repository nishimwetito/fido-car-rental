from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'price',
            'asset_type',
            'category',
            'listing_type',
            'location',
            'main_image',
        ]