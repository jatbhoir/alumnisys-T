"""
Posts URL Configuration
"""
from django.urls import path
from Posts import views
from .views import PostEditView, PostDeleteView

app_name = 'Posts'

urlpatterns = [
	path('', views.PostCommentCreateAndListView, name = 'all-posts'),
	path('liked/', views.LikeUnlikePosts, name = 'like-unlike-post' ),
	path('<pk>/edit/', PostEditView.as_view(), name = 'edit-post'),
	path('<pk>/delete/', PostDeleteView.as_view(), name = 'delete-post'),
]