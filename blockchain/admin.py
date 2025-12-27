from django.contrib import admin
from .models import BlockchainVerification


@admin.register(BlockchainVerification)
class BlockchainVerificationAdmin(admin.ModelAdmin):
    list_display = ['emission_entry', 'transaction_hash', 'network', 'verification_status', 'verified_at']
    list_filter = ['verification_status', 'network', 'verified_at']
    search_fields = ['transaction_hash', 'emission_entry__supplier__name']
    readonly_fields = ['transaction_hash', 'data_hash', 'verified_at']



