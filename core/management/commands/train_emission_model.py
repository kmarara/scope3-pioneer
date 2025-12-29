from django.core.management.base import BaseCommand
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib
import os
from pathlib import Path
from decimal import Decimal
from core.models import EmissionEntry, Supplier
from ml_services.models import MLModel

class Command(BaseCommand):
    help = 'Train a simple ML model for emission prediction'

    def handle(self, *args, **options):
        self.stdout.write('Training emission prediction model...')

        # Get historical data
        entries = EmissionEntry.objects.filter(
            verified=True
        ).select_related('supplier').order_by('date_reported')

        if entries.count() < 10:
            self.stdout.write(self.style.WARNING('Not enough data for training. Need at least 10 verified entries.'))
            return

        # Prepare features and target
        X = []  # Features: [supplier_id, month, year, previous_emissions]
        y = []  # Target: emissions

        supplier_emissions = {}
        for entry in entries:
            supplier_id = entry.supplier.id
            if supplier_id not in supplier_emissions:
                supplier_emissions[supplier_id] = []
            supplier_emissions[supplier_id].append({
                'date': entry.date_reported,
                'emissions': float(entry.scope3_emissions)
            })

        # Create time series features
        for supplier_id, emissions in supplier_emissions.items():
            if len(emissions) < 3:  # Need at least 3 data points
                continue

            emissions.sort(key=lambda x: x['date'])
            for i in range(2, len(emissions)):
                # Features: supplier_id, month, previous_2_emissions_avg
                prev_avg = (emissions[i-1]['emissions'] + emissions[i-2]['emissions']) / 2
                month = emissions[i]['date'].month
                X.append([supplier_id, month, prev_avg])
                y.append(emissions[i]['emissions'])

        if len(X) < 5:
            self.stdout.write(self.style.WARNING('Not enough time series data for training.'))
            return

        X = np.array(X)
        y = np.array(y)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        self.stdout.write(f'Model trained. RMSE: {rmse:.2f} tCO2e')

        # Save model
        model_dir = Path('ml_models')
        model_dir.mkdir(exist_ok=True)
        model_path = model_dir / 'emission_predictor.joblib'
        joblib.dump(model, model_path)

        # Save to database
        ml_model, created = MLModel.objects.get_or_create(
            name='Emission Time Series Predictor',
            defaults={
                'model_type': 'forecast',
                'version': '1.0',
                'model_path': str(model_path),
                'accuracy_score': Decimal(str(1 / (1 + rmse))),  # Simple accuracy metric
                'training_data_size': len(X_train),
                'metadata': {
                    'features': ['supplier_id', 'month', 'prev_2_avg_emissions'],
                    'rmse': rmse,
                    'algorithm': 'LinearRegression'
                }
            }
        )

        if not created:
            ml_model.version = '1.1'
            ml_model.accuracy_score = Decimal(str(1 / (1 + rmse)))
            ml_model.metadata = {
                'features': ['supplier_id', 'month', 'prev_2_avg_emissions'],
                'rmse': rmse,
                'algorithm': 'LinearRegression'
            }
            ml_model.save()

        self.stdout.write(self.style.SUCCESS(f'Model saved to {model_path}'))
        self.stdout.write(self.style.SUCCESS('ML model training completed!'))