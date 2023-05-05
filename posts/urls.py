from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.CreatePost.as_view(), name='create'),
    path('delete/<post_id>/<user_id>/', views.DeletePost.as_view(), name='delete'),
    path('like/<post_id>/', views.LikePost.as_view(), name='like'),
    path('dislike/<post_id>/', views.DislikePost.as_view(), name='dislike'),
]
