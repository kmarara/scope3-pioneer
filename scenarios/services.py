"""
Scenario modeling services
"""
from scenarios.models import Scenario, ScenarioSupplier
from core.models import Supplier, EmissionEntry
from django.db.models import Sum
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class ScenarioService:
    """Service for scenario modeling and what-if analysis"""
    
    @staticmethod
    def calculate_baseline_emissions(suppliers, period_start=None, period_end=None):
        """Calculate baseline emissions for suppliers"""
        entries = EmissionEntry.objects.filter(supplier__in=suppliers)
        
        if period_start:
            entries = entries.filter(date_reported__date__gte=period_start)
        if period_end:
            entries = entries.filter(date_reported__date__lte=period_end)
        
        total = entries.aggregate(total=Sum('scope3_emissions'))['total'] or Decimal('0')
        return total
    
    @staticmethod
    def calculate_scenario(scenario):
        """Calculate scenario reduction metrics"""
        # Get suppliers in scenario
        scenario_suppliers = ScenarioSupplier.objects.filter(scenario=scenario)
        suppliers = [ss.supplier for ss in scenario_suppliers]
        
        if not suppliers:
            # If no specific suppliers, use all tenant suppliers
            if scenario.tenant:
                suppliers = list(scenario.tenant.suppliers.all())
        
        # Calculate baseline
        baseline = ScenarioService.calculate_baseline_emissions(suppliers)
        
        # Calculate projected based on scenario type
        projected = ScenarioService.calculate_projected_emissions(
            scenario, suppliers, baseline
        )
        
        # Update scenario
        scenario.baseline_emissions = baseline
        scenario.projected_emissions = projected
        scenario.calculate_reduction()
        
        return {
            'baseline_emissions': float(baseline),
            'projected_emissions': float(projected),
            'reduction_amount': float(scenario.reduction_amount),
            'reduction_percentage': float(scenario.reduction_percentage),
        }
    
    @staticmethod
    def calculate_projected_emissions(scenario, suppliers, baseline):
        """Calculate projected emissions based on scenario type"""
        reduction_factor = Decimal('1.0')
        
        if scenario.scenario_type == 'renewable_energy':
            # Assume 30-50% reduction from renewable energy
            reduction_factor = Decimal('0.65')  # 35% reduction
        elif scenario.scenario_type == 'efficiency':
            # Assume 15-25% reduction from efficiency
            reduction_factor = Decimal('0.80')  # 20% reduction
        elif scenario.scenario_type == 'supplier_switch':
            # Assume 20-40% reduction from switching to lower-emission suppliers
            reduction_factor = Decimal('0.70')  # 30% reduction
        elif scenario.scenario_type == 'transport_optimization':
            # Assume 10-20% reduction from transport optimization
            reduction_factor = Decimal('0.85')  # 15% reduction
        
        # Allow custom reduction percentage
        if 'reduction_percentage' in scenario.parameters:
            custom_reduction = Decimal(str(scenario.parameters['reduction_percentage'])) / Decimal('100')
            reduction_factor = Decimal('1.0') - custom_reduction
        
        projected = baseline * reduction_factor
        return projected
    
    @staticmethod
    def create_scenario(name, scenario_type, tenant=None, suppliers=None, **kwargs):
        """Create a new scenario"""
        scenario = Scenario.objects.create(
            name=name,
            scenario_type=scenario_type,
            tenant=tenant,
            parameters=kwargs.get('parameters', {}),
        )
        
        if suppliers:
            baseline = ScenarioService.calculate_baseline_emissions(suppliers)
            projected = ScenarioService.calculate_projected_emissions(scenario, suppliers, baseline)
            
            scenario.baseline_emissions = baseline
            scenario.projected_emissions = projected
            scenario.calculate_reduction()
            
            # Create scenario supplier links
            for supplier in suppliers:
                supplier_baseline = ScenarioService.calculate_baseline_emissions([supplier])
                supplier_projected = supplier_baseline * (scenario.projected_emissions / scenario.baseline_emissions)
                
                ScenarioSupplier.objects.create(
                    scenario=scenario,
                    supplier=supplier,
                    baseline_emissions=supplier_baseline,
                    projected_emissions=supplier_projected,
                    reduction_percentage=scenario.reduction_percentage,
                )
        
        return scenario



