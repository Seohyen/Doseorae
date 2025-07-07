
from django.urls import path 
from . import views
urlpatterns = [
    path('book_list/', views.book_list),
    path('book_detail/<int:pk>/', views.book_detail),
    path('search_book/', views.search_book),
    path('interest_book/', views.interest_book),
    path('read_book/', views.read_book),
    path('get_top_20_books/', views.get_top_20_books)
]
