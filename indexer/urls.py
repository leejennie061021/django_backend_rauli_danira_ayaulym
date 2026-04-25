from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_podcast, name='add_podcast'),
    path('register/', views.register, name='register'),
    path('podcast/<int:podcast_id>/', views.podcast_detail, name='podcast_detail'),
    
    # --- Наши новые маршруты ---
    path('profile/', views.profile, name='profile'), 
    path('podcast/<int:podcast_id>/edit/', views.edit_podcast, name='edit_podcast'), 
    path('podcast/<int:podcast_id>/delete/', views.delete_podcast, name='delete_podcast'), 
    path('podcast/<int:podcast_id>/favorite/', views.toggle_favorite, name='toggle_favorite'), 
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # --- ФОРУМ ---
    path('forum/', views.forum_list, name='forum_list'), # Список всех тем
    path('forum/<int:topic_id>/', views.forum_topic, name='forum_topic'), # Конкретная тема
]