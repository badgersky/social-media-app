from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from follows.models import Follow
from users import forms, models
from posts.models import Tweet


class RegistrationView(View):

    def get(self, request):
        form = forms.RegistrationForm()
        return render(request, 'users/registration.html', {'form': form})

    def post(self, request):
        form = forms.RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Registration successful, please login.')

            return redirect(reverse('users:login'))

        return render(request, 'users/registration.html', {'form': form})


class LoginView(View):

    def get(self, request):
        form = forms.LoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = forms.LoginForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect(reverse('home:home'))

        return render(request, 'users/login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('home:home'))


class SearchUsersView(View):

    def get(self, request):
        username = request.GET.get('username')

        try:
            user = models.CustomUser.objects.get(username=username)
        except models.CustomUser.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'No such user!'
                                 )

            return redirect(reverse('home:home'))

        tweets = self.get_users_tweets(user)

        try:
            last_tweet = tweets[0]
        except IndexError:
            last_tweet = False

        return render(request, 'users/search.html', {'found_user': user, 'last_tweet': last_tweet})

    @staticmethod
    def get_users_tweets(user):
        try:
            tweets = Tweet.objects.filter(user=user).order_by('-date')
        except Tweet.DoesNotExist:
            tweets = False

        return tweets


class UserProfileView(View):

    def get(self, request, user_id):
        try:
            user = models.CustomUser.objects.get(pk=user_id)
        except models.CustomUser.DoesNotExist:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'No such user!'
                                 )

            return redirect(reverse('home:home'))

        tweets = SearchUsersView.get_users_tweets(user)

        if user == request.user:
            owner = True
            following = False
        else:
            owner = False
            following = False
            if Follow.objects.filter(followed_user=user, following_user=request.user).exists():
                following = True

        return render(request, 'users/profile.html', {'found_user': user,
                                                      'tweets': tweets,
                                                      'owner': owner,
                                                      'following': following})
