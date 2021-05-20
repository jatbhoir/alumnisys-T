#Django urls
from django.shortcuts import render, redirect, get_object_or_404
# Djando Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView
# Models
from .models import Job, Company, Category
from Accounts.models import Account
# Forms
from .forms import JobForm
#Other Imports
import datetime


# Jobs 
class JobListView(ListView):
	model = Job
	template_name = 'Jobs/jobs.html'


class JobDetailView(DetailView):
	model = Job
	template_name = 'Jobs/job_single.html'

	def get_object(self):
		get_object_or_404(Job, uuid = self.kwargs['uuid'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		job = Job.objects.get(uuid = self.kwargs['uuid'])
		user = self.request.user
		currentdatetime = datetime.datetime.now()

		context['user'] = user
		context['job'] = job
		context['uuid'] = self.kwargs['uuid']
		context['currentdatetime'] = currentdatetime

		return context

class AddJobView(CreateView):
	model = Job
	form_class = JobForm
	template_name = 'Jobs/add_job.html'


class UpdateJobView(UpdateView):
	model = Job
	form_class = JobForm
	template_name = 'Jobs/update_job.html'
	
	def get_object(self):
		get_object_or_404(Job, uuid = self.kwargs['uuid'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		job = Job.objects.get(uuid = self.kwargs['uuid'])
		user = self.request.user

		context['user'] = user
		context['job'] = job
		context['uuid'] = self.kwargs['uuid']

		return context