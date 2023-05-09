from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from follows.models import Follow
from users.models import CustomUser


class FollowUser(View):

    def get(self, request, user_id):
        if request.user.is_authenticated:
            try:
                followed_user = CustomUser.objects.get(pk=user_id)
            except CustomUser.DoesNotExist:
                next_ = request.get('next')

                messages.add_message(request,
                                     messages.WARNING,
                                     f'User you are trying to follow does not exist.'
                                     )
                return redirect(reverse(next_))

            if Follow.objects.filter(followed_user=followed_user, following_user=request.user).exists():
                return redirect(reverse('users:profile', kwargs={'user_id': user_id}))

            Follow.objects.create(followed_user=followed_user, following_user=request.user)
            followed_user.followers += 1
            followed_user.save()
            return redirect(reverse('users:profile', kwargs={'user_id': user_id}))
