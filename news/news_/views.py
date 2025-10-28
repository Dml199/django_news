
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django_filters.views import FilterView
from django.shortcuts import render, get_object_or_404,redirect
from .models import News, BaseRegisterForm,Category
from .templatetags.filters import NewsFilter
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User,Group
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib import messages

def news_list(request):
    news = News.objects.order_by('-pub_date')
    return render(request, 'news/news_list.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


def news_list(request):
    news_qs = News.objects.order_by('-created_at')
    articles = News.objects.filter(type__type = "Articles")
    news = News.objects.filter(type__type="News")
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
        'articles':articles,
        'news':news,
        
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
    
    def post(self,request, *args,**kwargs):

        news = News(
            
            user = request.user,
            title = request.POST['title'],
            content = request.POST['content'],
            type = Category.objects.get(id = request.POST['type'])
            
            
        )
        news.save()
        
        
        send_mail( 
            subject=f'{news.title} {news.user}',  # имя клиента и дата записи будут в теме для удобства
            message=f'{news.content}', 
            from_email='newACC-03@yandex.ru', # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['dmitrijladov396@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        return redirect(self.success_url)
    
    

        

        
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
    
@require_POST
@login_required
def subscribe_to_news_type(request):
    news_type = request.POST.get('news_type')
    # Находим все новости этого типа
    print(news_type)
    news_items = News.objects.filter(type__type=news_type)
    for news in news_items:
        news.subscribers.add(request.user)
    messages.success(request, f'Вы подписались на новости типа {news_type}')
    return redirect('post_list')  
    
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
  
