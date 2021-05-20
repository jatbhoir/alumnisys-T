"""
Friends URL Configuration
"""
from django.urls import path
from Friends import views

app_name = 'Friends'

urlpatterns = [
	path('friends/', views.RequestInviteFriendsListView, name='request-invite-friend'),
	path('friends/requests/', views.FriendRequestView, name='friend-request'),
	path('friends/friend-request/send/', views.sendInvitation, name='send-invite'),
	path('friends/friend-request/cancel/', views.cancelInvitation, name='cancel-invite'),
	path('friends/friend-request/accept/<friend_request_id>', views.acceptInvites, name='accept-invite'),
	path('friends/friend-request/reject/<friend_request_id>', views.rejectInvites, name='reject-invite'),
	path('friends/friend-request/delete/', views.removeFriend, name='remove-friend'),
	
]
