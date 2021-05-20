from django.contrib import admin
from .models import FriendList, FriendRequest

class FriendListAdmin(admin.ModelAdmin):
	list_display = ['user']
	list_filter = ['user']
	search_fields = ['user']
	readonly_fields = ['user']

	class Meta:
		model = FriendList

admin.site.register(FriendList, FriendListAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
	list_display = ['sender_id', 'receiver_id']
	list_filter = ['sender', 'receiver']
	search_fields = ['sender__username', 'receiver__username', 'sender__email', 'receiver__email']
	# readonly_fields = ['id']

	class Meta:
		model = FriendRequest

admin.site.register(FriendRequest, FriendRequestAdmin)
