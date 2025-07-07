from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)



class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    isbn = models.IntegerField()
    cover = models.CharField(max_length = 255)
    publisher = models.CharField(max_length=30)
    pub_date = models.DateField()
    author = models.CharField(max_length=100)
    author_info = models.TextField()
    author_photo = models.CharField(max_length = 255)
    customer_review_rank = models.FloatField()
    subTitle = models.CharField(max_length = 255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    voice_file = models.FileField(upload_to='voice/', blank=True, null=True)

