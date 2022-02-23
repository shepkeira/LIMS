from django import forms
from .models import SampleInspection, LabSample

class InspectionForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = SampleInspection
        fields = ('received_quantity', 'package_intact', 'material_intact', 'inspection_pass')

class DistributionForm(forms.ModelForm):
    """Form for the sample distribution"""
    class Meta:
        model = LabSample
        fields = ['location']