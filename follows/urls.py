from django.urls import path

from . import views

app_name = 'follows'

urlpatterns = [
    path('follow/<int:user_id>/', views.FollowUser.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', views.UnfollowUser.as_view(), name='unfollow'),
]
