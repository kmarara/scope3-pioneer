from django import forms
from .models import EmissionEntry

class EmissionEntryForm(forms.ModelForm):
    class Meta:
        model = EmissionEntry
        fields = ['supplier', 'date_reported', 'scope3_emissions', 'evidence_file', 'notes']
        widgets = {
            'date_reported': forms.DateInput(attrs={'type': 'date',
                                                    'class': 'form-control'}),}