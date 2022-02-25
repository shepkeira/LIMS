from django import forms
from .models import SampleInspection, TestResult

class InspectionForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = SampleInspection
        fields = ('received_quantity', 'package_intact', 'material_intact', 'inspection_pass')

class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ('status', 'result', 'pass_fail')