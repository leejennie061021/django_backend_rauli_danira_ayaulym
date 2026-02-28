from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_podcast, name='add_podcast'),
    path('register/', views.register, name='register'),
    path('podcast/<int:podcast_id>/', views.podcast_detail, name='podcast_detail'), # <-- НОВАЯ СТРОКА
]