from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EmissionEntryForm
from .models import EmissionEntry


# Create your views here.

def submit_emission(request):
    if request.method == 'POST':
        form = EmissionEntryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('submit_emission_success')
    else:
        form = EmissionEntryForm()
    return render(request, 'core/submit_emission.html', {'form': form})


def submit_emission_success(request):
    return render(request, 'core/submit_emission_success.html')


# View for login
@login_required
def emission_list(request):
    emissions = EmissionEntry.objects.all().order_by('-date_reported')
    return render(request, 'core/emission_list.html', {'emissions': emissions})