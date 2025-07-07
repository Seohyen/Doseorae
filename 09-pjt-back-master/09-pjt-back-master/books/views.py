from .serializers import BookListSerializer , BookDetailSerializer , BookRankList
from .models import Book,  Category
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import Count
from django.shortcuts import get_object_or_404
from gtts import gTTS
import os
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
import re
import unicodedata


# def slugify_filename(filename):
#     filename = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
#     filename = re.sub(r'[^\w\s-]', '', filename).strip().lower()
#     filename = re.sub(r'[-\s]+', '_', filename)
#     return filename

def generateTTS(text_content, book_instance):
    language = 'ko'
    speech = gTTS(text=text_content, lang=language, slow=False)

    audio_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
    os.makedirs(audio_dir, exist_ok=True)

    safe_title = book_instance.title
    filename = f"{safe_title}_audio.mp3"
    audio_path = os.path.join(audio_dir, filename)

    speech.save(audio_path)

    book_instance.voice_file.name = f"voice/{filename}"
    book_instance.save()


@api_view(['GET'])
def book_list(requset):
    books = Book.objects.all()

    
    serializer = BookListSerializer(books, many = True)
    return Response(serializer.data) 

@api_view(['GET'])
def book_detail(request,pk):
    book = Book.objects.get(pk=pk)
    audio_filename = f"{book.title}_audio.mp3"
    audio_dir = os.path.join(settings.MEDIA_ROOT, 'voice')
    audio_path = os.path.join(audio_dir, audio_filename)

    os.makedirs(audio_dir, exist_ok=True)

    if not os.path.exists(audio_path):
        generateTTS(book.description, book)

    serializer = BookDetailSerializer(book, context={'request': request})

    return Response(serializer.data)




@api_view(['POST'])
def search_book(request):
    title = request.data.get('title')
    
    if not title:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    books = Book.objects.filter(title__icontains=title)
    
    if not books.exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def interest_book(request):
    print("request.data:", request.data)
    try:
        bookPK = int(request.data.get("pk", ""))
    except (ValueError, TypeError):
        return Response({"error": "잘못된 pk 값입니다."}, status=400)

    try:
        book = Book.objects.get(pk=bookPK)
    except Book.DoesNotExist:
        return Response({'error': '해당 도서가 없습니다.'}, status=404)

    user = request.user
    if book in user.interestBooks.all(): 
        user.interestBooks.remove(book)
    else: 
        user.interestBooks.add(book)

    
    return Response(status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def read_book(request):
    print("request.data:", request.data)
    try:
        bookPK = int(request.data.get("pk", ""))
    except (ValueError, TypeError):
        return Response({"error": "잘못된 pk 값입니다."}, status=400)

    try:
        book = Book.objects.get(pk=bookPK)
    except Book.DoesNotExist:
        return Response({'error': '해당 도서가 없습니다.'}, status=404)

    user = request.user
    if book in user.read_books.all(): 
        user.read_books.remove(book)
    else: 
        user.read_books.add(book)

    
    return Response(status=200)

@api_view(['GET'])
def get_top_20_books(request):
    top_books = Book.objects.all().order_by('-customer_review_rank')[:20]
    serializer = BookRankList(top_books, many = True)

    return Response(serializer.data)

from dj_rest_auth.registration.views import RegisterView
from accounts.serializers import CustomRegisterSerializer

class MyRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
