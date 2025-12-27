from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from saas.models import Tenant


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your.email@company.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    organization_name = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Company Name'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'organization_name')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create tenant for the organization
            from django.utils.text import slugify
            org_name = self.cleaned_data['organization_name']
            tenant = Tenant.objects.create(
                name=org_name,
                slug=slugify(org_name),
                subscription_tier='free',
            )
            # Add user as tenant owner
            from saas.models import TenantUser
            TenantUser.objects.create(
                tenant=tenant,
                user=user,
                role='owner'
            )
        
        return user

