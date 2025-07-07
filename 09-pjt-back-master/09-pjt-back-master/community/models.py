from django.db import models
from django.conf import settings 
from books.models import Book

class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True) 

    def __str__(self):
        return self.name

class Thread(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_thread')
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  


