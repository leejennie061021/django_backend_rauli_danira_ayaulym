from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Podcast, Category, Comment, Rating, ForumTopic, ForumReply

# --- ФОРМА РЕГИСТРАЦИИ (НОВАЯ) ---
class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@gmail.com'}),
        help_text='Обязательно укажите email для восстановления пароля.'
    )

    class Meta:
        model = User
        fields = ('username', 'email')

# --- ФОРМЫ ДЛЯ ПОДКАСТОВ ---
class PodcastForm(forms.ModelForm):
    class Meta:
        model = Podcast
        fields = ['title', 'description', 'author', 'category', 'url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Краткое описание подкаста...', 'rows': 4}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Кто автор?'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Оставьте свой комментарий...', 'rows': 3}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.Select(attrs={'class': 'form-control', 'style': 'width: auto; display: inline-block; margin-right: 10px;'}),
        }

# --- ФОРМЫ ДЛЯ ПРОФИЛЯ ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'gender', 'phone_number', 'country']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 777 000 00 00'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Казахстан'}),
        }

# --- ФОРМЫ ДЛЯ ФОРУМА ---
class ForumTopicForm(forms.ModelForm):
    class Meta:
        model = ForumTopic
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название темы...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишите, что хотите обсудить...'}),
        }

class ForumReplyForm(forms.ModelForm):
    class Meta:
        model = ForumReply
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Написать ответ...'}),
        }