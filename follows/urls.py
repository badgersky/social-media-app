from django.urls import path

from . import views

app_name = 'follows'

urlpatterns = [
    path('<int:user_id>/', views.FollowUser.as_view(), name='follow'),
]
