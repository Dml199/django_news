from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class Author(models.Model):

    
    def __str__(self):
        return self.name
    
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # поле для текста новости
    author = models.ForeignKey(Author, on_delete=models.CASCADE)  # связь с автором
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    
class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")

    
    class Meta:
        model = User
        fields = ('username',
                 'first_name',
                 'last_name',
                 'email',
                 'password1',
                 'password2',
                 )