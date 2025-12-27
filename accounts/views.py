from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import UserRegistrationForm


def register(request):
    """User registration with automatic tenant creation"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created successfully! Welcome, {user.first_name}.')
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def profile(request):
    """User profile page"""
    return render(request, 'accounts/profile.html')

