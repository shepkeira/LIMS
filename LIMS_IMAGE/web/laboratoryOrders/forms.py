from django import forms
from .models import Inspection

class InspectionForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Inspection
        fields = ('package_integrity', 'material_integrity', 'inspection_results')