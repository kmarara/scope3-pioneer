"""
Custom API key authentication
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from saas.models import APIKey
from django.utils import timezone


class APIKeyAuthentication(BaseAuthentication):
    """Authenticate using API key"""
    
    def authenticate(self, request):
        api_key = request.META.get('HTTP_X_API_KEY') or request.GET.get('api_key')
        
        if not api_key:
            return None
        
        try:
            key_obj = APIKey.objects.get(key=api_key, is_active=True)
            
            # Check if expired
            if key_obj.is_expired():
                raise AuthenticationFailed('API key has expired')
            
            # Update last used
            key_obj.last_used = timezone.now()
            key_obj.save()
            
            # Return user and tenant
            return (key_obj.tenant, key_obj)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')



