from django.urls import path
from . import views
from .views import submit_emission

urlpatterns = [
    #submit-emission/
    path('', views.submit_emission, name='submit_emission'),
    path('submit-emission/success/', views.submit_emission_success, name='submit_emission_success'),
    path('emissions/', views.emission_list, name='emission_list'), # New table view
]

# new form is at http://127.0.0.1:8000/submit-emission/