"""
AWS Lambda function for batch ML predictions
Triggered by EventBridge on a schedule (e.g., daily)
"""
import json
import os
import boto3
from datetime import datetime, timedelta

# Initialize clients
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

# Environment variables
MODEL_BUCKET = os.environ.get('MODEL_BUCKET', 'scope3-ml-models')
PREDICTION_QUEUE = os.environ.get('PREDICTION_QUEUE', 'ml-predictions')
API_ENDPOINT = os.environ.get('API_ENDPOINT', 'https://api.scope3tracker.com')


def lambda_handler(event, context):
    """
    Run batch ML predictions for all active suppliers
    """
    try:
        # Get list of suppliers to process
        # In production, fetch from database or S3
        suppliers = get_suppliers_to_process()
        
        predictions = []
        for supplier in suppliers:
            prediction = generate_prediction(supplier)
            if prediction:
                predictions.append(prediction)
                # Send to queue for processing
                send_to_queue(prediction)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Generated {len(predictions)} predictions',
                'predictions': predictions
            })
        }
    
    except Exception as e:
        print(f"Error in batch prediction: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def get_suppliers_to_process():
    """
    Get list of suppliers that need predictions
    """
    # In production, query database or S3
    # For now, return mock data
    return [
        {'id': 1, 'name': 'Supplier A', 'region': 'Zimbabwe'},
        {'id': 2, 'name': 'Supplier B', 'region': 'South Africa'},
    ]


def generate_prediction(supplier):
    """
    Generate ML prediction for supplier
    """
    # Load model from S3
    model = load_model_from_s3('hotspot_model_v1.0.pkl')
    
    # Get supplier features
    features = get_supplier_features(supplier)
    
    # Generate prediction
    is_hotspot = model.predict([features])[0] == -1
    confidence = abs(model.score_samples([features])[0]) / 10.0
    confidence = min(max(confidence, 0.0), 1.0)
    
    return {
        'supplier_id': supplier['id'],
        'is_hotspot': bool(is_hotspot),
        'confidence': float(confidence),
        'timestamp': datetime.utcnow().isoformat(),
    }


def load_model_from_s3(model_name):
    """
    Load ML model from S3
    """
    import pickle
    
    try:
        response = s3.get_object(Bucket=MODEL_BUCKET, Key=model_name)
        model = pickle.loads(response['Body'].read())
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        # Return default model
        from sklearn.ensemble import IsolationForest
        return IsolationForest()


def get_supplier_features(supplier):
    """
    Get features for supplier (mock implementation)
    """
    # In production, fetch from database
    return [100.0, 500.0, 10, 120.0, 50000.0, 0.5, 1]


def send_to_queue(prediction):
    """
    Send prediction to SQS for async processing
    """
    try:
        sqs.send_message(
            QueueUrl=PREDICTION_QUEUE,
            MessageBody=json.dumps(prediction)
        )
    except Exception as e:
        print(f"Error sending to queue: {e}")



