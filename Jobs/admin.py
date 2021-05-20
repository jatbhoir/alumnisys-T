from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Job, Company, Category

class JobAdmin(ModelAdmin):
	list_display = ('owner', 'jobTitle', 'company', 'lastDate', 'created')
	search_fields = ('owner', 'company', 'lastDate')
	readonly_fields = ('uuid',)
	
	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Job, JobAdmin)

class CompanyAdmin(ModelAdmin):
	list_display = ('companyName', 'companyLocation')
	search_fields = ('companyName', 'companyLocation')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Company, CompanyAdmin)

admin.site.register(Category)