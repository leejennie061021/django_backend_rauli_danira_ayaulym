from django import forms
from .models import Podcast
class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['title', 'description', 'author', 'category', 'url'] # Добавили description
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Краткое описание подкаста...', 'rows': 4}), # Новое поле
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кто автор?'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
        }