from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import FileExtensionValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
from django.conf import settings
from django.utils import timezone

# Accounts
class AccountManager(BaseUserManager):
	# Creating User
	def create_user(self, username, email, password = None):
		if not username:
			raise ValueError("User must have an username.")
		if not email:
			raise ValueError("User must have an email address.")

		user = self.model(
				email = self.normalize_email(email),
				username = username,
		)
		user.set_password(password)
		user.save(using = self._db)
		print('New User Created: ', user)
		return user

	# Creating Super User
	def create_superuser(self, username, email, password):
		user = self.create_user(
				email = self.normalize_email(email),
				username = username,
				password = password,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		# user.set_password(password)
		user.save(using = self._db)
		return user

# Directory for Users Avatars.
def user_directory_path(instance, filename):
	return 'profile_pics/{0}/{1}/{2}'.format(instance.id, instance.username, filename)

class Account(AbstractBaseUser):
	# User Info
	first_name = models.CharField(max_length = 150, blank = True)
	last_name = models.CharField(max_length = 150, blank =True)
	username = models.CharField(max_length = 30, unique = True)
	email = models.EmailField(verbose_name = 'email', max_length = 60, unique = True)
	bio = models.TextField(max_length = 300, default = '', null = True, blank = True)
	website = models.CharField(max_length = 150, default = '', null = True, blank = True)
	phone = PhoneNumberField(default = '', null = True, blank = True)
	# For Admin Info
	last_login = models.DateTimeField(auto_now = True)
	date_joined = models.DateTimeField(auto_now_add = True)
	is_admin = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)
	# Extending Base Admin for User Info
	avatar = models.ImageField(upload_to = user_directory_path, default = 'avatar.png', validators = [FileExtensionValidator(['png', 'jpg', 'jpeg'])])
	grno = models.PositiveIntegerField(default = 1, blank = True, null = True)
	is_private = models.BooleanField(default = False)

	# Manager for Admin
	objects = AccountManager()

	# Default login/ register Parameters
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj = None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def get_absolute_url(self):
		# return reverse('Profiles:users-profile', args=[str(self.user.username)])
		return reverse('Accounts:users-profile', kwargs = {'username': self.username})

	def get_users_posts(self):
		return self.posts.all()


