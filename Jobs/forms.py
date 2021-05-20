from django import forms
from .models import Job, Company, Category
from ckeditor.widgets import CKEditorWidget

class JobForm(forms.ModelForm):
	class Meta:
		model = Job
		fields  = ('owner','jobTitle', 'jobDescription', 'jobURL', 'company', 'category', 'positionType', 'salary', 'lastDate')

		labels  = {
			'jobTitle':'Job Title:',
			'jobDescription':'Job Description:',
			'company':'Company:',
			'category':'Category:',
			'positionType':'Position Type:',
			'salary':'Salary:',
			'jobURL': 'Job URL:',
			'lastDate':'Last Date:',
		}

		widgets = {
			'owner' : forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'owner', 'type':'hidden'}),
			'jobTitle': forms.TextInput(attrs={'class': 'form-control'}),
			'company': forms.Select(attrs={'class': 'form-select'}),
			'category': forms.Select(attrs={'class': 'form-select'}),
			'positionType': forms.Select(attrs={'class': 'form-select'}),
			'jobURL': forms.TextInput(attrs={'class': 'form-control',}),
			'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'per annum.'}),
		}
