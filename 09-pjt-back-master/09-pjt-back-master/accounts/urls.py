from django.urls import path 
from . import views
from .views import MyRegisterView
urlpatterns = [
    path('follow/<int:pk>', views.follow),
    path('detail_user/', views.detailUser),
    path('user_profile/<int:pk>', views.user_profile),
    path('signup/', MyRegisterView.as_view(), name='custom_register')
]
