from django.db import models
from django.contrib.auth.models import User,Group
from django import forms
from django.contrib.auth.forms import UserCreationForm



class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # поле для текста новости
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



    
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    
    
    def save(self, commit=True, request=None):
     user = super(BaseRegisterForm, self).save(commit=commit)
     common_group = Group.objects.get(name='common')
     common_group.user_set.add(user)
     return user
        
    class Meta:
     model = User
     
     fields = ("username",)
