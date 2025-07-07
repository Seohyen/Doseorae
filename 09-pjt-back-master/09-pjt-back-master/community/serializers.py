from rest_framework import serializers
from .models import Thread , Comment, Hashtag
from .utils import create_or_get_hashtags , process_hashtags
from accounts.models import CustomUser
from books.models import Book

class ThreadListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_profile = serializers.ImageField(source='user.profile', read_only=True)
    def get_user_profile(self, obj):
        request = self.context.get('request')
        profile = getattr(obj.user, 'profile', None)
        if profile and hasattr(profile, 'url'):
            if request:
                return request.build_absolute_uri(profile.url)
            else:
                return profile.url  
        return None
    class Meta: 
        model = Thread
        fields = ['pk', 'title', 'user', 'username', 'user_profile', 'book_title']

class ThreadDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    hashtags = serializers.CharField(write_only=True, required=False, allow_blank=True)
    hashtag_list = serializers.SerializerMethodField()  
    username = serializers.CharField(source='user.username', read_only=True)
    user_profile = serializers.ImageField(source='user.profile', read_only=True)
    like_user_count = serializers.SerializerMethodField()
    user_profile = serializers.SerializerMethodField()
    book_title = serializers.CharField(source='book.title', read_only=True)
    def get_user_profile(self, obj):
        request = self.context.get('request')
        profile = getattr(obj.user, 'profile', None)
        if profile and hasattr(profile, 'url'):
            if request:
                return request.build_absolute_uri(profile.url)
            else:
                return profile.url  # fallback: 상대 경로라도 반환
        return None

    class Meta:
        model = Thread
        fields = '__all__'
        read_only_fields = ('book', 'user', 'created_at', 'updated_at', 'like_users', 'username', 'user_profile', 'book_title')
        extra_kwargs = {
            'hashtags': {'required': False},
        }
    
    def get_like_user_count(self, obj):
        return obj.like_users.count()
    
    
    def get_comments(self, obj):
        comments = obj.comment_set.all()
        return CommentListSerializer(comments, many=True).data

    def get_hashtag_list(self, obj):
        return [hashtag.name for hashtag in obj.hashtags.all()]

 
    def create(self, validated_data):
        hashtag_str = validated_data.pop('hashtags', '')  
        hashtags = process_hashtags(hashtag_str)          

        thread = Thread.objects.create(**validated_data)
        thread.hashtags.set(hashtags)
        return thread

    def update(self, instance, validated_data):
        hashtag_str = validated_data.pop('hashtags', '')
        hashtags = process_hashtags(hashtag_str)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.hashtags.set(hashtags)
        return instance
    def process_hashtags(hashtag_str):
        if not hashtag_str.strip():
            return []
        tags = hashtag_str.strip().split()
        return [create_or_get_hashtags(tag) for tag in tags]





class CommentSerializer(serializers.ModelSerializer):
    like_user_count = serializers.SerializerMethodField()
    user_profile = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)
    def get_user_profile(self, obj):
        request = self.context.get('request')
        profile = getattr(obj.user, 'profile', None)
        if profile and hasattr(profile, 'url'):
            if request:
                return request.build_absolute_uri(profile.url)
            else:
                return profile.url  # fallback: 상대 경로라도 반환
        return None

    class ThreadtitleSerializer(serializers.ModelSerializer):
        class Meta:
            model = Thread
            fields = ('title',)
    thread = ThreadtitleSerializer(read_only=True)         

    class Meta: 
        model = Comment
        fields = '__all__' 
        read_only_fields = ('user','thread','created_at','updated_at', 'like_users', 'user_profile', 'username')

    def get_like_user_count(self, obj):
        return obj.like_users.count() 
    


class CommentListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta: 
        model = Comment
        exclude = ['thread'] 
        read_only_fields = ('user','thread','created_at','updated_at', 'username')


class ThreadLikeSerializer(serializers.ModelSerializer): 
    like_users  = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='username'
    )
    like_thread  = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='username'
    )
    class Meta: 
        model = Thread
        fields = ['like_users', 'like_thread']


class CommentLikeSerializer(serializers.ModelSerializer): 
    like_users  = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='username'
    )
    like_comment  = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='username'
    )
    class Meta: 
        model = Thread
        fields  = ['like_users', 'like_comment']