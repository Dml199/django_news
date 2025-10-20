from django.urls import path
from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.BaseView.as_view(),name = 'base_view'),
    path('news/', views.news_list, name='news_list'),  # соответствует /news/
    path('news/search/', views.NewsSearchView.as_view(), name='news_search'),  # /news/search/
    path('news/create/', views.NewsCreateView.as_view(), name='news_create'),  # /news/create/
    path('news/<int:pk>/', views.news_detail, name='news_detail'),  # /news/<pk>/
    path('news/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='news_edit'),  # /news/<pk>/edit/
    path('news/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='news_delete'),  # /news/<pk>/delete/
    path('profile/', views.UserUpdateView.as_view(), name = 'user_view'),
    path('login/', views.LoginView.as_view(template_name = 'acc_forms/login.html'),  name = 'login'),
    path('logout/', views.LogoutView.as_view(template_name = 'acc_forms/logout.html'), name = 'logout'),
    path('register/',views.RegisterView.as_view(),name = 'signup'),
    path('accounts/',include('allauth.urls')),

    # Статьи
    path('articles/', views.ArticleListView.as_view(), name='articles_list'),
    path('articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('articles/create/', views.ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    
]