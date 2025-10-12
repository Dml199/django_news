

from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, TemplateView
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404
from .models import News, Article, BaseRegisterForm
from .templatetags.filters import NewsFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


def news_list(request):
    news = News.objects.order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    article = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'article': article})


def news_list(request):
    news_qs = News.objects.order_by('-created_at')
    paginator = Paginator(news_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    current = page_obj.number
    total = paginator.num_pages
    start = max(current - 2, 1)
    end = min(current + 2, total) + 1
    page_range = range(start, end)

    context = {
        'page_obj': page_obj,
        'page_range': page_range,
        'total_pages': total,
    }
    return render(request, 'news/news_list.html', context)

class NewsSearchView(FilterView):
    model = News
    template_name = 'news/news_search.html'
    filterset_class = NewsFilter
    paginate_by = 10

# CRUD для News
class NewsCreateView(CreateView):
    model = News
    fields = ['title', 'content', 'author']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

class NewsUpdateView(UpdateView):
    model = News
    fields = ['title', 'content', 'author']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('news_list')

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    success_url = reverse_lazy('news_list')

# CRUD для Article
class ArticleCreateView(CreateView):
    model = Article
    fields = ['title', 'content', 'author']
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')  # Создайте страницу списка статей

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ['title', 'content', 'author']
    template_name = 'articles/article_form.html'
    success_url = reverse_lazy('articles_list')

class ArticleDeleteView(DeleteView):
    model = Article
    template_name = 'articles/article_confirm_delete.html'
    success_url = reverse_lazy('articles_list')
    
    
class ArticleListView(ListView):
    model = Article
    template_name = 'articles/articles_list.html'  # создайте этот шаблон
    context_object_name = 'articles'  # имя в шаблоне
    
    
class ArticleDetailView(DetailView):
    model = Article
    template_name = 'articles/article_detail.html'  # создайте этот шаблон
    context_object_name = 'article'
    
    
class BaseView(TemplateView):
    template_name = 'base.html'
    
    
class UserUpdateView(UpdateView,LoginRequiredMixin):
    
    model = User
    template_name = 'profile_template/profile_view.html'
    
    
    
    
class LoginView(DetailView):
    
    template_name = 'login.html'
    
    
class RegisterView(CreateView):
    form_class = BaseRegisterForm
    model = User
    success_url = '/'
    template_name = 'acc_forms/register.html'
    
    