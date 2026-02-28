from django.db import models
from django.contrib.auth.models import User
import re

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Podcast(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True) # Новое поле
    author = models.CharField(max_length=255, verbose_name="Автор видео/подкаста")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    url = models.URLField(verbose_name="Ссылка на YouTube")
    uploader = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Кто загрузил", related_name='uploaded_podcasts')
    favorites = models.ManyToManyField(User, related_name='favorite_podcasts', blank=True) # Для избранного
    created_at = models.DateTimeField(auto_now_add=True)

    def get_youtube_id(self):
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', self.url)
        return match.group(1) if match else None

    def get_thumbnail_url(self):
        video_id = self.get_youtube_id()
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return "https://via.placeholder.com/640x360.png?text=No+Thumbnail"
        
    def get_average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.score for r in ratings) / len(ratings)
        return 0

    def __str__(self):
        return self.title

# --- НОВЫЕ МОДЕЛИ ---

class Rating(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)], verbose_name="Оценка (1-10)")

    class Meta:
        unique_together = ('podcast', 'user') # Чтобы один юзер мог поставить только одну оценку одному видео

class Comment(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True)

class ForumTopic(models.Model):
    title = models.CharField(max_length=255, verbose_name="Тема обсуждения")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ForumMessage(models.Model):
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name="Текст сообщения")
    created_at = models.DateTimeField(auto_now_add=True)