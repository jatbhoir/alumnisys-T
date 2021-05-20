# Django redirects or urls...
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
# Django Authentication
from django.contrib.auth import login, authenticate
# Django Views
from django.views import generic
from django.views.generic import ListView, DetailView
# Django Settings and Storage
from django.conf import settings
from django.core.files.storage import default_storage, FileSystemStorage
from django.core import files
# Django DBQuery
from django.db.models import Q
# Forms
from Accounts.forms import UserRegisterForm, UserUpdateForm
from Posts.forms import PostForm
# Models
from .models import Account
from Friends.models import FriendList, FriendRequest
# Other imports
from Friends.utils import get_friend_request_or_false
from Friends.status import FriendRequestStatus
import os
import cv2
import json
import base64
import requests

TEMP_PROFILE_IMAGE_NAME = "avatar.jpg"

# User Registration
def UserRegisterView(request, *args, **kwargs):
	user = request.user
	context = {}

	if request.POST:
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(username = username, password = raw_password)
			login(request, account)
			destination = kwargs.get('next')
			if destination:
				return redirect(destination)
			return redirect('login')
		else:
			context['form'] = form
	else:
		form = UserRegisterForm()
		context['form'] = form
	return render(request, 'Accounts/registration/register.html', context)

# Account
class AccountDetailView(DetailView):
	model = Account
	template_name = 'Profiles/users_profile.html'
	pk_url_kwarg = 'user__username'

	def post(self, request, *args, **kwargs):
	# Add Posts from Profile
		username = request.user.username
		if request.method == "POST":
			createPostForm = PostForm(request.POST, request.FILES)

			if createPostForm.is_valid():
				instance = createPostForm.save(commit = False)
				instance.author = request.user
				instance.save()

				self.object = self.get_object()
				context = super().get_context_data(**kwargs)
				context['createPostForm'] = PostForm

				return redirect('Accounts:users-profile', username)
			else:
				self.object = self.get_object()
				context = super(ProfileDetailView, self).get_context_data(**kwargs)
				context['createPostForm'] = PostForm

				return redirect('Accounts:users-profile', username)
			return self.render_to_response(context = context)

	def get_object(self):
		get_object_or_404(Account, username__iexact = self.kwargs['username'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		account = Account.objects.get(username__iexact = self.kwargs['username'])
		user = self.request.user

		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_request = None

		try:
			friends_list = FriendList.objects.get(user = account)
		except FriendList.DoesNotExist:
			friends_list = FriendList(user = account)
			friends_list.save()
		friends = friends_list.friends.all()

		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk = user.id):
				is_friend = True
			else:
				is_friend = False
				# CASE1: Request has been sent from THEM to YOU: FriendRequestStatus.THEM_SENT_TO_YOU
				if get_friend_request_or_false(sender = account, receiver = user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_req_id'] = get_friend_request_or_false(sender = account, receiver = user).id
				# CASE2: Request has been sent from YOU to THEM: FriendRequestStatus.YOU_SENT_TO_THEM
				elif get_friend_request_or_false(sender = user, receiver = account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				# CASE3: No request sent from YOU or THEM: FriendRequestStatus.NO_REQUEST_SENT
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_request = FriendRequest.objects.filter(receiver = user, is_active = True)
			except:
				pass


		context['users_id'] = account.id
		context['auth_user'] = user
		context['first_name'] = account.first_name
		context['last_name'] = account.last_name
		context['username'] = account.username
		context['email'] = account.email
		context['avatar'] = account.avatar
		context['bio'] = account.bio
		context['website'] = account.website
		context['phone'] = account.phone
		context['is_private'] = account.is_private
		
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['friends'] = friends
		context['request_sent'] = request_sent
		context['friend_request'] = friend_request

		context['createPostForm'] = PostForm
		context['posts'] = account.get_users_posts()
		context['len_posts'] = True if len(account.get_users_posts()) > 0 else False
		return context

# Search Friends via username or name?
def SearchFriend(request, *args, **kwargs):
	context = {}
	user = request.user
	if request.method == 'GET':
		searched = request.GET.get('q')
		if len(searched) > 0:
			search_result = Account.objects.filter(Q(username__icontains = searched) | Q(first_name__icontains = searched)).distinct()

			search_results = [] # [(account1, True), (account2, False), ...]
			if user.is_authenticated:
				# get the authenticated users friend list
				auth_user_friend_list = FriendList.objects.get(user=user)
				for account in search_result:
					search_results.append((account, auth_user_friend_list.is_mutual_friend(account)))
				context['search_results'] = search_results
			else:
				for account in search_result:
					accounts.append((account, False))
				context['search_results'] = search_results

		context['searched'] = searched
		return render(request, 'Profiles/search.html', context)

# Edit Profile
def EditProfileView(request):
	if not request.user.is_authenticated:
		return redirect('login')

	# profile = Account.objects.get(account = request.user)
	form = UserUpdateForm(request.POST or None, request.FILES or None, instance = request.user)
	confirm = False

	if request.method == 'POST':
		form = UserUpdateForm(request.POST or None, request.FILES or None, instance = request.user)
		if form.is_valid():
			form.save()
			confirm = True
		else:
			print(form.errors)
	else:
		form = UserUpdateForm(instance = request.user)

	context = {
		'user': request.user,
		'DATA_UPLOAD_MAX_MEMORY_SIZE': settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
		'form': form,
		'confirm': confirm,
	}
	return render(request, 'Accounts/edit_profile.html', context)

# Crop Avatar
def save_temp_avatar_from_base64String(imageString, user):
	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)
		image = base64.b64decode(imageString)
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None

def CropAvatar(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST and user.is_authenticated:
		try:
			imageString = request.POST.get("image")
			url = save_temp_avatar_from_base64String(imageString, user)
			print('og-url: ' + url)
			img = cv2.imread(url)

			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))

			if cropX < 0:
				cropX = 0
			if cropY < 0:
				cropY = 0
			crop_img = img[cropY: cropY + cropHeight, cropX: cropX + cropWidth]

			cv2.imwrite(url, crop_img)

			# user.avatar.delete(TEMP_PROFILE_IMAGE_NAME)
			user.avatar.save(TEMP_PROFILE_IMAGE_NAME, files.File(open(url, 'rb')))

			payload['result'] = "success"
			payload['cropped_avatar'] = user.avatar.url

			# os.remove(url)

		except Exception as e:
			payload['result'] = "error"
			payload['exception'] = str(e)

	return HttpResponse(json.dumps(payload), content_type = "application/json")
