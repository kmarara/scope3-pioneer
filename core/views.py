from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum, Avg, Count, Q
from django.utils import timezone
from datetime import timedelta

from .forms import EmissionEntryForm
from .models import EmissionEntry, Supplier
from django.core.paginator import Paginator
from ml_services.models import MLPrediction, SpendBasedEstimate
from scenarios.models import Scenario
from iot.models import IoTDevice, IoTReading

# Create your views here.

def home(request):
    """Home page - redirects to dashboard if logged in, shows landing page otherwise"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/home.html')


@login_required
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
    # http://127.0.0.1:8000/emissions/
    # Get filter values from GET request
    supplier_id = request.GET.get('supplier')
    verified = request.GET.get('verified')

    entries = EmissionEntry.objects.all().order_by('-date_reported')

    search_query = request.GET.get('search')
    if search_query:
        entries = entries.filter(notes__icontains=search_query)

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

    total_emissions = entries.aggregate(total=models.Sum('scope3_emissions'))['total'] or 0

    return render(request, 'core/emission_list.html',
                  {
                   'suppliers': suppliers,
                   'page_obj': page_obj,
                   'total_emissions': total_emissions,
                   })


@login_required
def dashboard(request):
    """Enhanced dashboard with ML insights and scenario modeling"""
    # Get user's tenant if applicable
    tenant = None
    if hasattr(request.user, 'tenant_membership'):
        tenant = request.user.tenant_membership.tenant
        suppliers = Supplier.objects.filter(tenant=tenant)
    else:
        suppliers = Supplier.objects.all()
    
    # Total emissions
    total_emissions = EmissionEntry.objects.filter(
        supplier__in=suppliers
    ).aggregate(total=Sum('scope3_emissions'))['total'] or 0
    
    # Recent emissions (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_emissions = EmissionEntry.objects.filter(
        supplier__in=suppliers,
        date_reported__gte=thirty_days_ago
    ).aggregate(total=Sum('scope3_emissions'))['total'] or 0
    
    # ML Hotspots
    hotspot_predictions = MLPrediction.objects.filter(
        supplier__in=suppliers,
        is_hotspot=True
    ).order_by('-confidence_score')[:5]
    
    # Top suppliers by emissions
    top_suppliers = EmissionEntry.objects.filter(
        supplier__in=suppliers
    ).values('supplier__name').annotate(
        total=Sum('scope3_emissions')
    ).order_by('-total')[:10]
    
    # IoT devices
    iot_devices = IoTDevice.objects.filter(supplier__in=suppliers, is_active=True)
    iot_device_count = iot_devices.count()
    
    # Recent IoT readings (last 24 hours)
    twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
    recent_readings = IoTReading.objects.filter(
        device__supplier__in=suppliers,
        timestamp__gte=twenty_four_hours_ago
    ).count()
    
    # Scenarios
    scenarios = Scenario.objects.filter(tenant=tenant).order_by('-created_at')[:5] if tenant else Scenario.objects.all()[:5]
    
    # Data source breakdown
    data_source_breakdown = EmissionEntry.objects.filter(
        supplier__in=suppliers
    ).values('data_source').annotate(
        count=Count('id'),
        total_emissions=Sum('scope3_emissions')
    )
    
    # Verification status
    verified_count = EmissionEntry.objects.filter(
        supplier__in=suppliers,
        verified=True
    ).count()
    blockchain_verified_count = EmissionEntry.objects.filter(
        supplier__in=suppliers,
        blockchain_verified=True
    ).count()
    total_entries = EmissionEntry.objects.filter(supplier__in=suppliers).count()
    
    context = {
        'total_emissions': total_emissions,
        'recent_emissions': recent_emissions,
        'hotspot_predictions': hotspot_predictions,
        'top_suppliers': top_suppliers,
        'iot_device_count': iot_device_count,
        'recent_readings': recent_readings,
        'scenarios': scenarios,
        'data_source_breakdown': data_source_breakdown,
        'verified_count': verified_count,
        'blockchain_verified_count': blockchain_verified_count,
        'total_entries': total_entries,
        'verification_rate': (verified_count / total_entries * 100) if total_entries > 0 else 0,
    }
    
    return render(request, 'core/dashboard.html', context)
