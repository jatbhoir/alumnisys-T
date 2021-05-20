#Django urls
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
# Djando Views
from django.views.generic import UpdateView, DeleteView
from django.template.loader import render_to_string
# Models
from .models import Post, Comment, Like
from Accounts.models import Account
# Forms
from .forms import PostForm, CommentForm
# Others
from django.contrib import messages
import json


# create Posts or Comments
def PostCommentCreateAndListView(request):
	user = request.user
	account = Account.objects.get(id = user.pk)
	posts = Post.objects.all()
	
	# comments = Comment.objects.filter(post = posts).order_by('-id')
	
	createPostForm = PostForm()
	createComment = CommentForm()

	if 'submit_post' in request.POST:
		createPostForm = PostForm(request.POST, request.FILES)
		if createPostForm.is_valid():
			instance = createPostForm.save(commit = False)
			instance.author = request.user
			instance.save()
			createPostForm = PostForm()
			return redirect('Posts:all-posts')
		else:
			createPostForm = PostForm()
			return redirect('Posts:all-posts')

	if 'submit_comment' in request.POST:
		createComment = CommentForm(request.POST)
		if createComment.is_valid():
			instance = createComment.save(commit = False)
			instance.user = request.user
			instance.post = Post.objects.get(id = request.POST.get('post_id'))
			instance.save()
			createComment = CommentForm()
			return redirect('Posts:all-posts')

	context = {
		'account': account,
		'posts': posts,
		'createPostForm': createPostForm,
		# 'comments':comments,
	}
	if request.is_ajax():
		html = render_to_string('Posts/comments.html', context, request = request)
		return JsonResponse({'form':html})

	return render(request, 'Posts/posts.html', context)

def LikeUnlikePosts(request):
	if request.method == 'POST':
		post_id = request.POST.get('post_id')
		post_obj = Post.objects.get(id = post_id)
		account =  request.user

		if account in post_obj.likes.all():
			post_obj.likes.remove(account)
		else:
			post_obj.likes.add(account)

		like, created = Like.objects.get_or_create(user = account, post_id = post_id)

		if not created:
			if like.value == 'Like':
				like.value = 'Unlike'
			else:
				like.value = 'Like'
		else:
			like.value = 'Like'

			post_obj.save()
			like.save()

		return redirect('Posts:all-posts')

# Editing or Deleting a Post
class PostEditView(UpdateView):
	model = Post
	# form_class = PostForm
	fields = ['content']
	template_name = 'Posts/snippets/editPost.html'
	success_url = reverse_lazy('Posts:all-posts')

	def form_valid(self, form):
		user = self.request.user
		if form.instance.author == user:
			return super().form_valid(form)
		else:
			form.add_error(None, 'You Need to be the user of this Post')
			return super().form_invalid(form)

class PostDeleteView(DeleteView):
	model = Post
	template_name = 'Posts/snippets/deletePost.html'
	success_url = reverse_lazy('Posts:all-posts')

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk = pk)
		if not obj.author == self.request.user:
			messages.warning(self.request, 'You Need to be the user of this Post')
		return obj

# Editing and Deleting a Comment/Comments...
