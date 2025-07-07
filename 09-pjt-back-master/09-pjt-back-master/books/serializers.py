from rest_framework import serializers
from .models import Book, Category
import os
from django.conf import settings
from pathlib import PurePosixPath

class BookListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Book
        fields = ['pk','title', 'cover', 'author', 'publisher', 'pub_date', 'category']
        read_only = 'voice_file'

class BookDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    voice_url = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'  
        read_only = 'voice_file'
    def get_voice_url(self, obj):
        request = self.context.get('request')
        if obj.voice_file and request:
            return request.build_absolute_uri(obj.voice_file.url)
        return None
class BookRankList(serializers.ModelSerializer): 
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field = 'name'
    )
    class Meta: 
        model = Book
        fields = ['pk','title','cover','author','publisher','category', 'customer_review_rank']




class InterestBook(serializers.ModelSerializer):
    class Meta:
        model = Book               
        fields = ['id', 'title','cover']   


class ReadBook(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['pk', 'title', 'cover']