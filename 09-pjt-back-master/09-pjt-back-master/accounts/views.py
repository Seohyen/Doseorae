from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import UserSerializer
from .models import CustomUser
from accounts.serializers import CustomRegisterSerializer
from dj_rest_auth.registration.views import RegisterView


@api_view(['GET'])
def detailUser(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    serializer = UserSerializer(request.user, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
def user_profile(request, pk): 
    user = CustomUser.objects.get(pk = pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request, pk):
    User = get_user_model()

    you = User.objects.get(pk=pk)
    me = request.user
    if you != me:  
        if you in me.followings.all(): 
            me.followings.remove(you)  
        else:
            me.followings.add(you) 

 
    serializer = UserSerializer(me)
    return Response(serializer.data)  

class MyRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer