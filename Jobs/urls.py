"""
Jobs URL Configuration
"""
from django.urls import path
# from Jobs import views
from .views import JobListView, JobDetailView, AddJobView, UpdateJobView

app_name = 'Jobs'

urlpatterns = [
	# path('', JobListView.as_view() , name='job-lists'),
	path('add/', AddJobView.as_view() , name='add-job'),
	path('<uuid>/', JobDetailView.as_view() , name='job-single'),
	path('<uuid>/update/', UpdateJobView.as_view() , name='update-job'),
	# path('<uuid:pk>/', JobDetailView.as_view() , name='job-single'),
]