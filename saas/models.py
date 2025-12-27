from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import secrets


class Tenant(models.Model):
    """Multi-tenant organization model for SaaS"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, help_text="URL-friendly identifier")
    domain = models.CharField(max_length=255, blank=True, help_text="Custom domain (optional)")
    subscription_tier = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Free'),
            ('starter', 'Starter'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='free'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    max_suppliers = models.IntegerField(default=10, help_text="Maximum number of suppliers")
    max_users = models.IntegerField(default=3, help_text="Maximum number of users")
    features = models.JSONField(default=dict, blank=True, help_text="Enabled features")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.subscription_tier})"
    
    def can_add_supplier(self):
        """Check if tenant can add more suppliers"""
        from core.models import Supplier
        current_count = Supplier.objects.filter(tenant=self).count()
        return current_count < self.max_suppliers
    
    def can_add_user(self):
        """Check if tenant can add more users"""
        current_count = TenantUser.objects.filter(tenant=self).count()
        return current_count < self.max_users


class TenantUser(models.Model):
    """Links users to tenants with roles"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='tenant_users')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_membership')
    role = models.CharField(
        max_length=50,
        choices=[
            ('owner', 'Owner'),
            ('admin', 'Admin'),
            ('member', 'Member'),
            ('viewer', 'Viewer'),
        ],
        default='member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tenant', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.tenant.name} ({self.role})"


class APIKey(models.Model):
    """API keys for programmatic access"""
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=255, help_text="Descriptive name for the key")
    key = models.CharField(max_length=64, unique=True, help_text="API key")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.tenant.name}"
    
    @staticmethod
    def generate_key():
        """Generate a secure API key"""
        return secrets.token_urlsafe(48)
    
    def is_expired(self):
        """Check if API key is expired"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class Subscription(models.Model):
    """Subscription management"""
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=50, choices=Tenant.subscription_tier.field.choices)
    status = models.CharField(
        max_length=50,
        choices=[
            ('active', 'Active'),
            ('cancelled', 'Cancelled'),
            ('expired', 'Expired'),
            ('trial', 'Trial'),
        ],
        default='trial'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, help_text="Stripe subscription ID")
    
    def __str__(self):
        return f"{self.tenant.name} - {self.plan} ({self.status})"
    
    def is_active(self):
        """Check if subscription is currently active"""
        return self.status == 'active' and timezone.now() < self.current_period_end
    
    def renew(self, months=1):
        """Renew subscription"""
        self.current_period_end = timezone.now() + timedelta(days=30 * months)
        self.status = 'active'
        self.save()



