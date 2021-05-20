"""
Accounts URL Configuration
"""
from django.urls import path
from Accounts import views
from .views import AccountDetailView

app_name = 'Accounts'

urlpatterns = [
	path('', AccountDetailView.as_view(), name='users-profile'),
]
