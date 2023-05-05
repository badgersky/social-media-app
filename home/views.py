from django.shortcuts import render
from django.views import View
from posts.models import Tweet


class HomeView(View):

    def get(self, request):
        tweets = Tweet.objects.all().order_by('-date')

        return render(request, 'home/home.html', {'tweets': tweets})
