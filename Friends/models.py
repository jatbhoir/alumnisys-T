from djongo import models
from django.conf import settings
from django.utils import timezone
from Accounts.models import Account


# Friend Requests
class FriendList(models.Model):

	user = models.OneToOneField(Account, on_delete = models.CASCADE, related_name = 'user')
	friends = models.ManyToManyField(Account, blank = True, related_name = 'friends')

	def __str__(self):
		return self.user.username

	def add_friend(self, account):
		# add friend to Flist
		if not account in self.friends.all():
			self.friends.add(account)

	def remove_friend(self, account):
		# remove friend to Flist
		if account in self.friends.all():
			self.friends.remove(account)

	def unfriend(self, removee):
		# remover is the person removing and removee is the person getting removed as friend
		# remove removee from removers Flist
		removers_flist = self
		removers_flist.remove_friend(removee)
		# remove remover from removees Flist
		friends_list = FriendList.objects.get(user = removee)
		friends_list.remove_friend(self.user)

	def is_mutual_friend(self, friend):
		if friend in self.friends.all():
			return True
		return False

class FriendRequest(models.Model):

	sender = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'sender')
	receiver = models.ForeignKey(Account, on_delete = models.CASCADE, related_name = 'receiver')
	is_active = models.BooleanField(default = True, blank = False, null = False)
	timestamp = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.sender.username

	def accept(self):
		# Accept a Friend Request
		receiver_flist = FriendList.objects.get(user = self.receiver)
		if receiver_flist:
			receiver_flist.add_friend(self.sender)
			sender_flist = FriendList.objects.get(user = self.sender)
			if sender_flist:
				sender_flist.add_friend(self.receiver)
				self.is_active = False
				self.save()
		



