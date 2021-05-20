from djongo import models
from django.core.validators import FileExtensionValidator
from Accounts.models import Account


def user_directory_path(instance, filename):
	return 'posts/{0}/{1}/{2}'.format(instance.author.id,instance.author.username, filename)

class Post(models.Model):
	author = models.ForeignKey(Account, related_name = 'posts', on_delete = models.CASCADE)
	content = models.TextField()
	image = models.ImageField(upload_to = user_directory_path, validators = [FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank = False)
	likes = models.ManyToManyField(Account, blank = True, related_name = 'likes')
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return str(self.content[:20])

	def num_likes(self):
		return self.likes.all().count()

	def num_comments(self):
		return self.comment_set.all().count()

	class Meta:
		ordering = ('-created',)

class Comment(models.Model):
	user = models.ForeignKey(Account, on_delete = models.CASCADE)
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	user_comment = models.TextField(max_length = 300)
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "User: {} | Comment: {} | Commented To: {}".format(self.user, self.user_comment, self.post)

	class Meta:
		ordering = ('-created',)

LIKE_CHOICES = (
	('Like', 'Like'),
	('Unlike', 'Unlike')
)

class Like(models.Model):
	user = models.ForeignKey(Account, on_delete = models.CASCADE)
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	value = models.CharField(max_length = 8, choices = LIKE_CHOICES)
	updated = models.DateTimeField(auto_now = True)
	created = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return "User:{} | Post:{} | Value:{}".format(self.user, self.post, self.value)
