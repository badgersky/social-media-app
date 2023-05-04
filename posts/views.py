from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from . import forms


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
