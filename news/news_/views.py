from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import News

def news_list(request):
    news = News.objects.order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    article = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'article': article})