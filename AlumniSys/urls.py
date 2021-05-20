"""AlumniSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Views...
from django.contrib.auth import views as auth_views
from Accounts import views as account_views
from Friends import views as friend_views # FriendsListView
from Jobs import views as job_views

# Urls..
urlpatterns = [
	path('admin/', admin.site.urls),

	# Auth urls
	path('accounts/register/', account_views.UserRegisterView, name='register'),
	path('accounts/login/', auth_views.LoginView.as_view(template_name='Accounts/registration/login.html'), name='login'),
	path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('accounts/password/change/', auth_views.PasswordChangeView.as_view(template_name='Accounts/registration/password_change.html'), name='password_change'),
	path('accounts/password/change/done', auth_views.PasswordChangeDoneView.as_view(template_name='Accounts/registration/password_change_done.html'), name='password_change_done'),
	path('accounts/password/reset/', auth_views.PasswordResetView.as_view(template_name='Accounts/registration/password_reset.html'), name='password_reset'),
	path('accounts/password/reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Accounts/registration/password_reset_done.html'), name='password_reset_done'),
	path('accounts/password/reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='Accounts/registration/password_reset_confirm.html'), name='password_reset_confirm'),
	path('accounts/password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/registration/password_reset_complete.html'), name='password_reset_complete'),
	path('accounts/edit/', account_views.EditProfileView, name='edit-profile'),
	path('accounts/edit/crop/', account_views.CropAvatar, name='crop-avatar'),

	# Posts urls
	path('posts/', include('Posts.urls')),

	# Jobs url
	path('job/', include('Jobs.urls')),
	path('jobs/', job_views.JobListView.as_view() , name='job-lists'),
	

	# Events url
	# path('event/', include('Events.urls')),

	# Friends urls
	path('<str:username>/friends/', friend_views.FriendsListView.as_view(), name='friends'),
	path('', include('Friends.urls')),

	# Accounts
	path('search/', account_views.SearchFriend, name='search'),
	path('<str:username>/', include('Accounts.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
