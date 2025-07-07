
from django.urls import path 
from . import views
urlpatterns = [
    path('', views.threadList),
    path('detail/<int:pk>', views.threadDetailView),
    path('create_thread/<int:pk>', views.createThread),
    path('detail/<int:thread_pk>/create_comment/', views.createComment),
    path('detail/<int:thread_pk>/detail_comment/<int:pk>', views.commentDetailView),
    path('like_thread/<int:pk>', views.like_thread),
    path('like_comment/<int:pk>', views.like_comment)
    
]
