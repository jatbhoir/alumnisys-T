from django.contrib import admin
from .models import Post, Comment, Like

# Register your models here.

#Make Manager
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)