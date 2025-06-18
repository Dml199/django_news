from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

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
    
