from django.db import models
from django.contrib.auth.models import User,Group
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

class Category(models.Model):
    type = models.CharField( max_length = 100, choices = [('News','Articles')] ,default = "News")
    subscribers = models.ManyToManyField(User, related_name='subs', blank=True)
    def __str__(self):
        return self.type

class News(models.Model):
   
    title = models.CharField(max_length = 200)
    type= models.ForeignKey( Category , on_delete = models.CASCADE)
    content = models.TextField()  # поле для текста новости
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
  
    def __str__(self):
        return self.title



    
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email",required = True)
    
    
    def save(self, commit=True, request=None):
     user = super(BaseRegisterForm, self).save(commit=commit)
     common_group = Group.objects.get(name='common')
     common_group.user_set.add(user)
     return user
        
    class Meta:
     model = User
     
     fields = ("username","email")
