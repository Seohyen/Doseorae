from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import CustomUser, Category
from books.serializers import InterestBook , ReadBook

class UserSerializer(serializers.ModelSerializer):
    followings = serializers.SlugRelatedField(
        many=True, 
        read_only=True, 
        slug_field='username'
    )
    followers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )
    likeCategory = serializers.SlugRelatedField(
        queryset=Category.objects.all(),  
        slug_field='name',              
        required=False,
        allow_null=True,
    )
    interestBooks = InterestBook(many=True, read_only=True)
    read_books = ReadBook(many = True, read_only=True)
    profile = serializers.ImageField(use_url=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'level', 'exp', 'maxExp', 'likeCategory', 'password', 'followings', 'followers', 'interestBooks', 'profile', 'nickName','read_books']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
    

class CustomRegisterSerializer(RegisterSerializer):
    nickName = serializers.CharField(required=True)
    profile = serializers.ImageField(required=False, allow_null=True)
    likeCategory = serializers.SlugRelatedField(
        queryset=Category.objects.all(),  
        slug_field='name',               
        required=False,
        allow_null=True,
    )
    def __init__(self, *args, **kwargs):
        print("CustomRegisterSerializer __init__ 호출됨")
        super().__init__(*args, **kwargs)

    def validate(self, data):
        print("CustomRegisterSerializer validate 호출됨:", data)
        return super().validate(data)
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['nickName'] = self.validated_data.get('nickName', '')
        data['profile'] = self.validated_data.get('profile', None)
        data['likeCategory'] = self.validated_data.get('likeCategory', None)  # 여기에 추가
        return data

    def custom_signup(self, request, user):
        user.nickName = self.validated_data.get('nickName', '')
        user.profile = self.validated_data.get('profile', None)
        user.likeCategory = self.validated_data.get('likeCategory', None)  # 여기에 추가
        user.save(update_fields=['nickName', 'profile', 'likeCategory'])