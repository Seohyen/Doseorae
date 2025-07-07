from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings 
from books.models import Book
from books.models import Category


class CustomUser(AbstractUser):
    level = models.IntegerField(default=1)  
    exp = models.IntegerField(default=0)   
    maxExp = models.IntegerField(default = 30)
    likeCategory = models.ForeignKey(Category, on_delete=models.CASCADE, blank = True, null = True) 
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, symmetrical=False, related_name='followers')
    interestBooks = models.ManyToManyField(Book, blank=True, related_name='interested_users')
    read_books = models.ManyToManyField(Book, blank=True, related_name='read_users')
    profile = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    nickName = models.CharField(max_length=50)