from django.db import models
from django.contrib.auth.models import User


class Media(models.Model):
    CATEGORY_CHOICES = (
        ('physics', 'Physics'),
        ('biology', 'Biology'),
        ('chemistry', 'Chemistry'),
        ('tech', 'Technology'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField()
    thumbnail = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
