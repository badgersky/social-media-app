from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from posts.models import Tweet


class HomeView(View):

    def get(self, request):
        tweets = Tweet.objects.all().order_by('-date')
        paginator = Paginator(tweets, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'home/home.html', {'page_obj': page_obj})
