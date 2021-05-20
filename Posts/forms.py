from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields  = ('content', 'image')

		widgets = {
			'content': forms.Textarea(attrs={'class': 'form-control glass', 'rows':'3'}),
			'image': forms.FileInput(attrs={'class': 'form-control glass',}),
		}

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('user_comment',)