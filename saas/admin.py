from django.contrib import admin
from .models import Tenant, TenantUser, APIKey, Subscription


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'subscription_tier', 'is_active', 'max_suppliers', 'max_users']
    list_filter = ['subscription_tier', 'is_active']
    search_fields = ['name', 'slug']


@admin.register(TenantUser)
class TenantUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'tenant', 'role', 'joined_at']
    list_filter = ['role', 'tenant']
    search_fields = ['user__username', 'tenant__name']


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ['name', 'tenant', 'is_active', 'created_at', 'last_used', 'expires_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'key', 'tenant__name']
    readonly_fields = ['key', 'created_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'plan', 'status', 'started_at', 'current_period_end']
    list_filter = ['plan', 'status']
    search_fields = ['tenant__name']



