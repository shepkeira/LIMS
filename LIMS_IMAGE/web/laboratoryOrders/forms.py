from django import forms
from .models import SampleInspection, TestResult, Sample

class InspectionForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = SampleInspection
        fields = ('received_quantity', 'package_intact', 'material_intact', 'inspection_pass')

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ('status', 'result', 'test_pass')

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ('sample_type', 'sample_form', 'sop_number')