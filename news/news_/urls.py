from django.urls import path
from . import views
from django.urls import path,include

urlpatterns = [
    path('', views.BaseView.as_view(),name = 'base_view'),
    path('posts/', views.news_list, name='post_list'), 
    path('posts/search/', views.NewsSearchView.as_view(), name='post_search'),  
    path('posts/create/', views.NewsCreateView.as_view(), name='post_create'),  
    path('posts/<int:pk>/', views.news_detail, name='post_detail'),  
    path('posts/<int:pk>/edit/', views.NewsUpdateView.as_view(), name='post_edit'),  
    path('posts/<int:pk>/delete/', views.NewsDeleteView.as_view(), name='post_delete'),  
    path('profile/', views.UserUpdateView.as_view(), name = 'user_view'),
    path('login/', views.LoginView.as_view(template_name = 'acc_forms/login.html'),  name = 'login'),
    path('logout/', views.LogoutView.as_view(template_name = 'acc_forms/logout.html'), name = 'logout'),
    path('register/',views.RegisterView.as_view(),name = 'signup'),
    path('accounts/',include('allauth.urls')),
    path('add_author/', views.add_to_authors_group, name= 'add_author')
]