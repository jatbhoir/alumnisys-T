import uuid
from djongo import models
from django.core.validators import FileExtensionValidator
from django.shortcuts import reverse
from ckeditor.fields import RichTextField
from Accounts.models import Account


def company_directory_path(instance, filename):
	return 'company/{0}/{1}/'.format(instance.companyName, filename)

class Company(models.Model):

	companyName = models.CharField(max_length = 255)
	companyLogo = models.ImageField(upload_to = company_directory_path, default = 'company.jpg', validators = [FileExtensionValidator(['png', 'jpg', 'jpeg'])])
	#companyDescription = RichTextField(blank = True, null = True)
	companyLocation = models.CharField(max_length = 150)
	seoDescription = models.TextField(blank = True, null = True)
	seoKeywords = models.TextField(blank = True, null = True)

	def __str__(self):
		return self.companyName +' | '+ str(self.companyLocation)

class Category(models.Model):

	categoryName = models.CharField(max_length = 255)

	def __str__(self):
		return str(self.categoryName)

JOB_TYPE = (
    ('Part Time', 'Part Time'),
    ('Full Time', 'Full Time'),
)

class Job(models.Model):

	owner = models.ForeignKey(Account, on_delete=models.CASCADE, related_name = 'owner') 
	company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name = 'company')
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name = 'category')
	jobTitle = models.CharField(max_length = 255)
	jobDescription = RichTextField(blank = True, null = True)
	jobURL = models.URLField(max_length = 300)
	# jobDescription = models.TextField(blank = True, null = True)
	uuid = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
	positionType = models.CharField(choices=JOB_TYPE, max_length=10)
	salary = models.CharField(max_length=100, null=True, blank=True)
	lastDate = models.DateTimeField(null=True, blank=True) 
	created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.jobTitle +' | '+ str(self.owner)

	def get_absolute_url(self):
		return reverse('Jobs:job-single', kwargs = {'uuid': self.uuid})

	class Meta:
		ordering = ('-created',)






