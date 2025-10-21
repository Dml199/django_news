

from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404,redirect
from .models import News, BaseRegisterForm
from .templatetags.filters import NewsFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,Group
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required


def news_list(request):
    news = News.objects.order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


def news_list(request):
    news_qs = News.objects.order_by('-created_at')
    articles = News.objects.filter(type = "Articles")
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
        'articles':articles
    }
    return render(request, 'news/news_list.html', context)

class NewsSearchView(FilterView):
    model = News
    template_name = 'news/news_search.html'
    filterset_class = NewsFilter
    paginate_by = 10

# CRUD для News
class NewsCreateView(PermissionRequiredMixin, LoginRequiredMixin,CreateView):
    model = News
    permission_required = ('news_.add_news')
    fields = ['title', 'content', 'type']
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('post_list')
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) 

class NewsUpdateView(PermissionRequiredMixin, LoginRequiredMixin,UpdateView):
    model = News
    fields = ['title', 'content']
    permission_required = ('news_.change_news')
    template_name = 'news/news_form.html'
    success_url = reverse_lazy('post_list')
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) 

class NewsDeleteView(LoginRequiredMixin,DeleteView):
    model = News
    template_name = 'news/news_confirm_delete.html'
    permission_required = ('news_.delete_news')
    success_url = reverse_lazy('post_list')
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super().form_valid(form) 
    
class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News
    template_name = 'news/news_detail.html'  # создайте этот шаблон
    context_object_name = 'article'

    
class BaseView(TemplateView):
    template_name = 'base.html'
    
    
class UserUpdateView(LoginRequiredMixin,UpdateView):
    login_url = "/login/"
    def get_object(self):
        return self.request.user
    
    def get_initial(self):
        initial = super().get_initial()
        
        initial['password'] = ''
        return initial
    
    def form_valid(self, form):
        user = form.save(commit=False)
        raw_password = form.cleaned_data.get('password')
        if raw_password:
            user.set_password(raw_password)  # hash new password
        else:
            # If password is empty, keep existing password (avoid overwrite)
            user.password = self.get_object().password
        user.save()
        return super().form_valid(form)

    
    fields= ["username", "password"]
    success_url = "/"
    model = User
    template_name = 'profile_template/profile_view.html'
    
    
    
class RegisterView(CreateView):
    form_class = BaseRegisterForm
  
    model = User

    success_url = '/'
    template_name = 'acc_forms/register.html'
    

@login_required
def add_to_authors_group(request):

    user = request.user
    group, created = Group.objects.get_or_create(name='authors')
    user.groups.add(group)
    return redirect('/') 
  
