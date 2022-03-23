from django import forms
from .models import Image, Location, Test

class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('image',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'code')

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('name', 'sample_type', 'code', 'cost', 'time_taken', 'limit')