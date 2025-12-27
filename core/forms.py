from django import forms
from .models import EmissionEntry

class EmissionEntryForm(forms.ModelForm):
    date_reported = forms.DateTimeField(
        widget=forms.TextInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Choose date of report'
            }),
        label='Reporting Date'
    )

    scope3_emissions = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g 104.5'
        }),
        label='Scope 3 CO₂ Emission (tons)',
        help_text='Enter the total CO₂ in metric tons. Ex 104.5'
    )

    evidence_file = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        label='Supporting Document (PDF .docx, or image)'
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Optional: any context/comments...'
        }),
        label='Additional Comments'
    )

    class Meta:
        model = EmissionEntry
        fields = ['supplier', 'date_reported', 'scope3_emissions', 'evidence_file', 'notes']
        labels = {
            'supplier': 'Supplier Name'
        }
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-select'}),
        }
        #widgets = {
            #'date_reported': forms.DateInput(attrs={'type': 'date',
                                                    #'class': 'form-control'}),}