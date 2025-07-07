from django.urls import path 
from . import views
urlpatterns = [
    path('ask_gpt', views.ask_gpt),
    path('quize_gpt', views.quizeGpt),
    path('debate_gpt', views.debateGpt),
    path('update_exp', views.updatePlayerLevel )
]
