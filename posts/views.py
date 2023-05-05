from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from . import forms
from . import models
from users.models import CustomUser


class CreatePost(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('users:login'))

        form = forms.CreatePostForm(initial={'user': request.user.id, 'likes': 0})

        return render(request, 'posts/create-post.html', {'form': form})

    def post(self, request):
        form = forms.CreatePostForm(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                post = form.save(commit=False)
                user = request.user

                post.user = user
                post.save()

                return redirect(reverse('home:home'))

        return render(request, 'posts/create-post.html', {'form': form})


class DeletePost(View):

    def get(self, request, post_id, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return redirect(reverse('home:home'))

        if request.user.is_authenticated and request.user == user:
            try:
                post = models.Tweet.objects.get(pk=post_id, user_id=user_id)
            except models.Tweet.DoesNotExist:
                return redirect(reverse('users:profile', kwargs={'user_id': user_id}))

            post.delete()

            messages.add_message(request,
                                 messages.SUCCESS,
                                 f'Post deleted successfully.'
                                 )

            return redirect(reverse('users:profile', kwargs={'user_id': user_id}))
        else:
            return redirect(reverse('users:login'))


class LikePost(View):

    def get(self, request, post_id):
        referer = request.headers.get('Referer')

        try:
            tweet = models.Tweet.objects.get(pk=post_id)
        except models.Tweet.DoesNotExist:
            return redirect(reverse('home:home'))

        if not request.user.is_authenticated:
            messages.add_message(request,
                                 messages.WARNING,
                                 f'You must be logged in in order to like post.',
                                 )

            return redirect(reverse('users:login'))

        if models.TweetLikes.objects.filter(tweet=tweet, user=request.user).exists():
            return redirect(referer)

        if tweet.user == request.user:
            return redirect(referer)

        tweet.likes += 1
        tweet.save()
        models.TweetLikes.objects.create(tweet=tweet, user=request.user)
        return redirect(referer)
