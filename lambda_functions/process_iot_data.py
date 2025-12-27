"""
AWS Lambda function for processing IoT data
This function can be triggered by IoT Core, SQS, or EventBridge
"""
import json
import os
import boto3
from decimal import Decimal

# Initialize clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sqs = boto3.client('sqs')

# Environment variables
API_ENDPOINT = os.environ.get('API_ENDPOINT', 'https://api.scope3tracker.com')
IOT_TABLE = os.environ.get('IOT_TABLE', 'iot-readings')


def lambda_handler(event, context):
    """
    Process IoT data from various sources
    """
    try:
        # Handle different event sources
        if 'Records' in event:
            # SQS or DynamoDB Streams
            for record in event['Records']:
                if 'body' in record:
                    # SQS message
                    data = json.loads(record['body'])
                    process_iot_reading(data)
                elif 'dynamodb' in record:
                    # DynamoDB stream
                    data = record['dynamodb']['NewImage']
                    process_iot_reading(data)
        elif 'device_id' in event:
            # Direct API Gateway invocation
            process_iot_reading(event)
        else:
            # IoT Core rule
            process_iot_reading(event)
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'IoT data processed successfully'})
        }
    
    except Exception as e:
        print(f"Error processing IoT data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


def process_iot_reading(data):
    """
    Process a single IoT reading
    """
    device_id = data.get('device_id')
    energy_kwh = Decimal(str(data.get('energy_kwh', 0)))
    
    # Calculate emissions (simplified - in production, use region-specific factors)
    emission_factor = Decimal('0.5')  # kg CO2e per kWh (default)
    emissions_kg = energy_kwh * emission_factor
    emissions_tons = emissions_kg / Decimal('1000')
    
    # Store in DynamoDB for fast access
    table = dynamodb.Table(IOT_TABLE)
    table.put_item(
        Item={
            'device_id': device_id,
            'timestamp': data.get('timestamp'),
            'energy_kwh': str(energy_kwh),
            'emissions_tons': str(emissions_tons),
            'processed': True,
        }
    )
    
    # Send to main API for persistence
    # In production, use API Gateway or direct database connection
    send_to_api(data, emissions_tons)
    
    return {
        'device_id': device_id,
        'emissions_tons': float(emissions_tons),
    }


def send_to_api(data, emissions_tons):
    """
    Send processed data to main Django API
    """
    import urllib.request
    import urllib.parse
    
    api_data = {
        'device_id': data.get('device_id'),
        'api_key': data.get('api_key'),
        'energy_kwh': data.get('energy_kwh'),
        'power_kw': data.get('power_kw'),
        'voltage': data.get('voltage'),
        'current': data.get('current'),
        'temperature': data.get('temperature'),
        'metadata': data.get('metadata', {}),
    }
    
    # In production, use proper HTTP client with authentication
    # For now, this is a placeholder
    pass



