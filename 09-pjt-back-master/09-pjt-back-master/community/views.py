from .serializers import ThreadListSerializer, ThreadDetailSerializer , CommentSerializer, ThreadLikeSerializer, CommentLikeSerializer
from .models import Thread , Comment
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from books.models import Book

@api_view(['GET'])
def threadList(request):
    threads = Thread.objects.all()
    serializer = ThreadListSerializer(threads, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def threadDetailView(request, pk):
    thread = get_object_or_404(Thread, pk=pk)

    if request.method == 'GET':
        serializer = ThreadDetailSerializer(thread, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT': 
        serializer = ThreadDetailSerializer(thread, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


    elif request.method == 'DELETE':
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createThread(request, pk):
    book = get_object_or_404(Book, pk=pk)
    serializer = ThreadDetailSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(book=book, user=request.user)
        updatePlayerLevel(request.user , 'thread')
        return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createComment(request, thread_pk): 
    thread = get_object_or_404(Thread, pk=thread_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(thread=thread, user=request.user)
        updatePlayerLevel(request.user , 'comment')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def commentDetailView(request, thread_pk,  pk ): 
    comment = get_object_or_404(Comment, pk = pk)
    thread = Thread.objects.get(pk = thread_pk)
    if request.method == 'GET': 
        serializer = CommentSerializer(comment, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PUT': 
        serializer =  CommentSerializer(comment, data = request.data)
        serializer.save(thread  = thread , user = request.user) 
        return Response(serializer.data)
    elif request.method == 'DELETE': 
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_thread(request, pk): 
    thread = get_object_or_404(Thread, pk = pk)
    user= request.user
    serializer = ThreadLikeSerializer(thread)

    if user in thread.like_users.all(): 
        thread.like_users.remove(user)
    else:
        thread.like_users.add(user)
    return Response(serializer.data) 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk = pk)
    user= request.user
    serializer = CommentLikeSerializer(comment)

    if user in comment.like_users.all(): 
        comment.like_users.remove(user)
    else:
        comment.like_users.add(user)
    return Response(serializer.data) 


def updatePlayerLevel(user, state):
    if state == 'thread': 
        user.exp += 10
    elif state == 'comment':
        user.exp += 5
    while user.exp >= user.maxExp:
        user.level += 1
        user.exp -= user.maxExp
        user.maxExp = int(user.maxExp * 1.5)
    user.save()
