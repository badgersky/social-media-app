from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('search/', views.SearchUsersView.as_view(), name='search'),
    path('profile/<user_id>/', views.UserProfileView.as_view(), name='profile')
]
