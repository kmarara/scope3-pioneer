from django.shortcuts import render
from .forms import EmissionEntryForm


# Create your views here.

def submit_emission(request):
    if request.method == 'POST':
