from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from core.models import Supplier, EmissionEntry
from saas.models import Tenant
from django.contrib.auth.models import User
from saas.models import TenantUser

class Command(BaseCommand):
    help = 'Populate database with sample data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample tenant if none exists
        if not Tenant.objects.exists():
            tenant = Tenant.objects.create(
                name='Demo Corporation',
                slug='demo-corp',
                subscription_tier='free'
            )
            self.stdout.write(f'Created tenant: {tenant.name}')
        else:
            tenant = Tenant.objects.first()

        # Create sample user if none exists
        if not User.objects.filter(username='demo_user').exists():
            user = User.objects.create_user(
                username='demo_user',
                email='demo@demo.com',
                password='demo123',
                first_name='Demo',
                last_name='User'
            )
            TenantUser.objects.create(
                tenant=tenant,
                user=user,
                role='owner'
            )
            self.stdout.write(f'Created user: {user.username}')

        # Create sample suppliers
        suppliers_data = [
            {'name': 'Steel Manufacturing Co', 'region': 'North America', 'industry': 'Manufacturing', 'email': 'steel@demo.com'},
            {'name': 'Green Energy Solutions', 'region': 'Europe', 'industry': 'Energy', 'email': 'green@demo.com'},
            {'name': 'Logistics Plus', 'region': 'Asia', 'industry': 'Transportation', 'email': 'logistics@demo.com'},
            {'name': 'Tech Components Ltd', 'region': 'Asia', 'industry': 'Technology', 'email': 'tech@demo.com'},
            {'name': 'Paper Products Inc', 'region': 'North America', 'industry': 'Manufacturing', 'email': 'paper@demo.com'},
        ]

        suppliers = []
        for data in suppliers_data:
            supplier, created = Supplier.objects.get_or_create(
                contact_email=data['email'],
                defaults={
                    'name': data['name'],
                    'region': data['region'],
                    'industry': data['industry'],
                    'tenant': tenant,
                    'supplier_code': f"SUP{random.randint(1000,9999)}",
                    'annual_spend': Decimal(random.uniform(100000, 1000000)),
                    'emission_factor': Decimal(random.uniform(0.1, 1.0)),
                }
            )
            suppliers.append(supplier)
            if created:
                self.stdout.write(f'Created supplier: {supplier.name}')

        # Create sample emission entries
        for i in range(50):
            supplier = random.choice(suppliers)
            days_ago = random.randint(0, 365)
            date = timezone.now() - timedelta(days=days_ago)

            # Generate realistic emission values based on industry
            base_emission = {
                'Manufacturing': random.uniform(100, 1000),
                'Energy': random.uniform(50, 500),
                'Transportation': random.uniform(200, 1500),
                'Technology': random.uniform(20, 200),
            }.get(supplier.industry, random.uniform(50, 500))

            EmissionEntry.objects.get_or_create(
                supplier=supplier,
                date_reported=date,
                defaults={
                    'scope3_emissions': Decimal(str(round(base_emission, 2))),
                    'notes': f'Sample emission data for {supplier.name}',
                    'verified': random.choice([True, False]),
                }
            )

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
        self.stdout.write('Login with: demo_user / demo123')