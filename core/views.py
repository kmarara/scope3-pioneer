from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EmissionEntryForm
from .models import EmissionEntry, Supplier
from django.core.paginator import Paginator

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
#@login_required
def emission_list(request):
    # http://127.0.0.1:8000/emissions/
    # Get filter values from GET request
    supplier_id = request.GET.get('supplier')
    verified = request.GET.get('verified')


    entries = EmissionEntry.objects.all().order_by('-date_reported')

    if supplier_id:
        entries = entries.filter(supplier__id=supplier_id)

    if verified == "true":
        entries = entries.filter(verified=True)

    elif verified == "false":
        entries = entries.filter(verified=False)

    # For filter dropdown
    suppliers = Supplier.objects.all()

    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'core/emission_list.html',
                  {
                   'suppliers': suppliers,
                   'page_obj': page_obj
                   })