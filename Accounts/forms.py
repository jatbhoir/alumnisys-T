from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Account

# Custom Validations
def ForbiddenUsers(value):
	forbidden_users = ['admin', 'authenticate', 'login', 'logout', 'administrator', 'root',
						'email', 'user', 'sql', 'static', 'delete']
	if value.lower() in forbidden_users:
		raise ValidationError('Invalid name for user, this is a reserverd word. Try something else.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not use these chars: @, -, +')

# UserCreationForm
class UserRegisterForm(UserCreationForm):
	email  = forms.EmailField(max_length = 255, help_text = "Required. Add a valid email address.")

	class Meta:
		model = Account
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)

		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.get(email = email)
		except Account.DoesNotExist:
			return email
		raise ValidationError('Email already exists')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.get(username = username)
		except Account.DoesNotExist:
			return username
		raise ValidationError('Username already exists.')

	def clean_password(self):
		super(UserRegisterForm, self).clean()
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')

		if password1 != password2:
			self._errors['password'] = self.error_class(['Passwords do not match. Try again.'])
		return self.cleaned_data

class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ['avatar','first_name', 'last_name', 'username', 'email', 'phone', 'website', 'bio']

	def __init__(self, *args, **kwargs):
		super(UserUpdateForm, self).__init__(*args, **kwargs)

	def clean(self):
		self.fields['username'].validators.append(ForbiddenUsers)
		self.fields['username'].validators.append(InvalidUser)

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk = self.instance.pk).get(email = email)
		except Account.DoesNotExist:
			return email
		raise ValidationError('Email already exists')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk = self.instance.pk).get(username = username)
		except Account.DoesNotExist:
			return username
		raise ValidationError('Username already exists.')

	# def save(self, commit = True):
	#     account = super(UserUpdateForm, self).save(commit = False)
	#     account.avatar = self.cleaned_data['avatar']
	#     account.first_name = self.cleaned_data['first_name']
	#     account.last_name = self.cleaned_data['last_name']
	#     account.username = self.cleaned_data['username']
	#     account.email = self.cleaned_data['email']
	#     account.phone = self.cleaned_data['phone']
	#     account.website = self.cleaned_data['website']
	#     account.bio = self.cleaned_data['bio']
	#     if commit:
	#         account.save()
	#     return account
