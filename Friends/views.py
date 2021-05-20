# Django redirects or urls...
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# Django Views
from django.views import generic
from django.views.generic import ListView, DetailView
# Models
from .models import FriendList, FriendRequest
from Accounts.models import Account
# Other imports
from .utils import get_friend_request_or_false
from .status import FriendRequestStatus
from django.db.models import Q
import json


# listView of friends (say. people you might know page) and users friend request
def RequestInviteFriendsListView(request, *args, **kwargs):
	context = {}
	user = request.user
	account = Account.objects.get(username = request.user.username)

	# Friend Requests
	if user.is_authenticated:
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver = account, is_active = True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("You cannot view Someone elses Friend requests.")
	else:
		redirect('login')

	all_friends = Account.objects.all().exclude(username = request.user.username)
	context['all_friends'] = all_friends

	# People you might know...

	return render(request, 'Friends/friend_request_or_invite.html', context)
	
# friend request page where you can Accept or reject invites
def FriendRequestView(request, *args, **kwargs):
	context = {}
	user = request.user
	account = Account.objects.get(username = request.user.username)

	if user.is_authenticated:
		if account == user:
			friend_requests = FriendRequest.objects.filter(receiver = account, is_active = True)
			context['friend_requests'] = friend_requests
		else:
			return HttpResponse("You cannot view Someone elses Friend requests.")
	else:
		redirect('login')
	return render(request, 'Friends/friends_request.html', context)

class FriendsListView(ListView):
	model = Account
	template_name = 'Friends/friends.html'

	def get_object(self):
		return get_object_or_404(Account, username__iexact = self.kwargs['username'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		account = Account.objects.get(username__iexact = self.kwargs['username'])
		user = self.request.user

		# Friends List
		try:
			friend_list = FriendList.objects.get(user = account)
		except FriendList.DoesNotExist:
			return HttpResponse(f"Could not find the friends list for {account}")

		Friends = []
		auth_user_flist = FriendList.objects.get(user = user)
		for friend in friend_list.friends.all():
			Friends.append((friend, auth_user_flist.is_mutual_friend(friend)))

		context['Friends'] = Friends
		context['account'] = account
		context['users_id'] = account.id


		return context

# send friend request to somebody(friend?) # ADD A Friend
def sendInvitation(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk = user_id)
			try:
				friend_requests = FriendRequest.objects.filter(sender = user, receiver = receiver)
				try:
					for request in friend_requests:
						if request.is_active:
							raise Exception("You already sent them a Friend Request.")
					friend_request = FriendRequest(sender = user, receiver = receiver)
					friend_request.save()
					payload['response'] = "Friend Request Sent."
				except Exception as e:
					payload['response'] = str(e)
			except FriendRequest.DoesNotExist:
				friend_request = FriendRequest(sender = user, receiver = receiver)
				friend_request.save()
				payload['response'] = "Friend Request Sent."

			if payload['response'] == None:
				payload['response'] = "Something went wrong."
		else:
			payload['response'] = "Unable to sent a Friend Request."
	else:
		payload['response'] = "You must be Authenticated to send a Friend rRequest."
	return HttpResponse(json.dumps(payload), content_type="application/json")

# accept friend request from sent by someone(received request) # ACCEPT Friend Request
def acceptInvites(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk = friend_request_id)
			if friend_request.receiver == user:
				if friend_request:
					friend_request.accept()
					payload['response'] = "Friend Request Accepted."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to Accept."
		else:
			payload['response'] = "Unable to Accept the Friend Request."
	else:
		payload['response'] = "You must be Authenticated to Accept a Friend Request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

# reject friend request from sent by someone(received request) # REJECT Friend Request
def rejectInvites(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "GET" and user.is_authenticated:
		friend_request_id = kwargs.get("friend_request_id")
		if friend_request_id:
			friend_request = FriendRequest.objects.get(pk = friend_request_id)
			if friend_request.receiver == user:
				if friend_request:
					friend_request.delete()
					payload['response'] = "Friend Request Rejected."
				else:
					payload['response'] = "Something went wrong."
			else:
				payload['response'] = "That is not your request to Reject."
		else:
			payload['response'] = "Unable to Reject the Friend Request."
	else:
		payload['response'] = "You must be Authenticated to Reject a Friend Request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

# cancel friend request # CANCEL A Friend Request sent by you.
def cancelInvitation(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			receiver = Account.objects.get(pk = user_id)
			try:
				friend_request = FriendRequest.objects.get((Q(sender = user) & Q(receiver = receiver)) | (Q(sender = receiver) & Q(receiver = user)))
				friend_request.delete()
				payload['response'] = "Friend Request Cancelled."
			except Exception as e:
				payload['response'] = "Friend Request Does Not Exist."
		else:
			payload['response'] = "Unable to Cancel the Friend Request."
	else:
		payload['response'] = "You must be Authenticated to Cancel the Friend Request."
	return HttpResponse(json.dumps(payload), content_type="application/json")

# remove friend from your FriendList and Others FriendList # REMOVE FRIEND
def removeFriend(request, *args, **kwargs):
	user = request.user
	payload = {}
	if request.method == "POST" and user.is_authenticated:
		user_id = request.POST.get("receiver_user_id")
		if user_id:
			try:
				removee = Account.objects.get(pk = user_id)
				friend_list = FriendList.objects.get(user = user)
				friend_list.unfriend(removee)
				friend_request = FriendRequest.objects.get((Q(sender = user) & Q(receiver = removee)) | (Q(sender = removee) & Q(receiver = user)))
				friend_request.delete()
				payload['response'] = "Friend Removed."
			except Exception as e:
				payload['response'] = "Something went wrong. " + str(e)
		else:
			payload['response'] = "Unable to Remove the Friend "
	else:
		payload['response'] = "You must be Authenticated to Remove the Friend "
	return HttpResponse(json.dumps(payload), content_type="application/json")