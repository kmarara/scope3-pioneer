"""
ML Services for emission prediction and hotspot detection
"""
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils import timezone
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from django.conf import settings
from django.db.models import Avg, Sum, Count
from core.models import EmissionEntry, Supplier
from ml_services.models import MLModel, MLPrediction, SpendBasedEstimate
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class HotspotPredictor:
    """Predicts emission hotspots using ML"""
    
    def __init__(self, model_version='1.0'):
        self.model_version = model_version
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = os.path.join(settings.ML_MODELS_DIR, f'hotspot_model_v{model_version}.pkl')
        self.load_or_train()
    
    def load_or_train(self):
        """Load existing model or train new one"""
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded hotspot model from {self.model_path}")
            except Exception as e:
                logger.error(f"Error loading model: {e}")
                self.train()
        else:
            self.train()
    
    def prepare_features(self, suppliers):
        """Prepare features for prediction"""
        features = []
        for supplier in suppliers:
            # Get historical data
            entries = EmissionEntry.objects.filter(supplier=supplier)
            if not entries.exists():
                continue
            
            avg_emissions = entries.aggregate(avg=Avg('scope3_emissions'))['avg'] or 0
            total_emissions = entries.aggregate(total=Sum('scope3_emissions'))['total'] or 0
            entry_count = entries.count()
            recent_emissions = entries.order_by('-date_reported')[:3]
            recent_avg = sum([e.scope3_emissions for e in recent_emissions]) / len(recent_emissions) if recent_emissions else 0
            
            # Supplier features
            spend = float(supplier.annual_spend) if supplier.annual_spend else 0
            emission_factor = float(supplier.emission_factor) if supplier.emission_factor else 0
            
            feature_vector = [
                float(avg_emissions),
                float(total_emissions),
                entry_count,
                float(recent_avg),
                spend,
                emission_factor,
                1 if supplier.region else 0,  # Has region
            ]
            features.append((supplier, feature_vector))
        
        return features
    
    def train(self):
        """Train hotspot detection model"""
        logger.info("Training hotspot prediction model...")
        
        # Get all suppliers with emission data
        suppliers = Supplier.objects.filter(emission_entries__isnull=False).distinct()
        
        if suppliers.count() < 10:
            logger.warning("Insufficient data for training. Using default model.")
            self.model = IsolationForest(contamination=0.1, random_state=42)
            return
        
        features_data = self.prepare_features(suppliers)
        if not features_data:
            logger.warning("No features prepared. Using default model.")
            self.model = IsolationForest(contamination=0.1, random_state=42)
            return
        
        X = np.array([f[1] for f in features_data])
        
        # Use Isolation Forest for anomaly/hotspot detection
        self.model = IsolationForest(contamination=0.15, random_state=42)
        self.model.fit(X)
        
        # Save model
        os.makedirs(settings.ML_MODELS_DIR, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Model saved to {self.model_path}")
    
    def predict_hotspot(self, supplier):
        """Predict if supplier is a hotspot"""
        features_data = self.prepare_features([supplier])
        if not features_data:
            return False, 0.5
        
        X = np.array([features_data[0][1]])
        prediction = self.model.predict(X)[0]
        score = self.model.score_samples(X)[0]
        
        # Normalize score to 0-1 (higher = more likely hotspot)
        is_hotspot = prediction == -1
        confidence = abs(score) / 10.0  # Rough normalization
        confidence = min(max(confidence, 0.0), 1.0)
        
        return is_hotspot, confidence


class SpendBasedEstimator:
    """Estimates emissions based on spend and industry factors"""
    
    # Industry emission factors (tCO2e per $1000 USD spend)
    INDUSTRY_FACTORS = {
        'manufacturing': Decimal('0.45'),
        'transport': Decimal('0.65'),
        'energy': Decimal('0.85'),
        'construction': Decimal('0.35'),
        'agriculture': Decimal('0.25'),
        'technology': Decimal('0.15'),
        'retail': Decimal('0.20'),
        'default': Decimal('0.30'),
    }
    
    @staticmethod
    def estimate_emissions(supplier, spend_amount, period_start, period_end):
        """Estimate emissions from spend"""
        # Get industry factor
        industry = supplier.industry.lower() if supplier.industry else 'default'
        factor = SpendBasedEstimator.INDUSTRY_FACTORS.get(industry, SpendBasedEstimator.INDUSTRY_FACTORS['default'])
        
        # Use supplier's emission factor if available, otherwise use industry default
        if supplier.emission_factor:
            emission_factor = supplier.emission_factor
        else:
            emission_factor = factor
        
        # Calculate: spend in $1000 * factor = tCO2e
        spend_in_thousands = Decimal(str(spend_amount)) / Decimal('1000')
        estimated_emissions = spend_in_thousands * emission_factor
        
        # Create estimate record
        estimate = SpendBasedEstimate.objects.create(
            supplier=supplier,
            period_start=period_start,
            period_end=period_end,
            spend_amount=spend_amount,
            emission_factor=emission_factor,
            estimated_emissions=estimated_emissions,
            industry_category=industry,
        )
        
        return estimate


class MLPredictionService:
    """Service for managing ML predictions"""
    
    @staticmethod
    def create_prediction(supplier, model_type='hotspot', period_start=None, period_end=None):
        """Create ML prediction for supplier"""
        
        
        if not period_start:
            period_start = timezone.now().date()
        if not period_end:
            period_end = period_start + timedelta(days=365)
        
        # Get or create model
        model, _ = MLModel.objects.get_or_create(
            model_type=model_type,
            defaults={
                'name': f'{model_type.title()} Model',
                'version': '1.0',
                'is_active': True,
            }
        )
        
        if model_type == 'hotspot':
            predictor = HotspotPredictor()
            is_hotspot, confidence = predictor.predict_hotspot(supplier)
            
            # Get average emissions for prediction
            entries = EmissionEntry.objects.filter(supplier=supplier)
            avg_emissions = entries.aggregate(avg=Avg('scope3_emissions'))['avg'] or Decimal('0')
            
            prediction = MLPrediction.objects.create(
                supplier=supplier,
                model=model,
                predicted_emissions=avg_emissions,
                confidence_score=confidence,
                is_hotspot=is_hotspot,
                hotspot_reason="High emission intensity detected" if is_hotspot else "",
                period_start=period_start,
                period_end=period_end,
                input_features={
                    'annual_spend': float(supplier.annual_spend) if supplier.annual_spend else 0,
                    'emission_factor': float(supplier.emission_factor) if supplier.emission_factor else 0,
                    'region': supplier.region or '',
                }
            )
            
            return prediction
        
        return None
