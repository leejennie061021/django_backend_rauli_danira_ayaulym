from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseForbidden
from .models import Podcast
from .forms import PodcastForm
from .models import Podcast, Comment, Rating
from .forms import PodcastForm, CommentForm, RatingForm
from .forms import PodcastForm, CommentForm, RatingForm, UserUpdateForm, UserProfileForm
from .models import Podcast, Category, Comment, Rating, UserProfile, ForumTopic, ForumReply
from .forms import (
    PodcastForm, 
    CommentForm, 
    RatingForm, 
    UserUpdateForm, 
    UserProfileForm, 
    ForumTopicForm, 
    ForumReplyForm, 
    SignUpForm  # <--- Обязательно добавь её сюда
)
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Podcast, Category

def index(request):
    query = request.GET.get('q') # Получаем текст поиска
    cat_id = request.GET.get('category') # Получаем ID категории
    
    podcasts_list = Podcast.objects.all().order_by('-id') # Сначала самые новые

    # 1. Поиск по названию
    if query:
        podcasts_list = podcasts_list.filter(title__icontains=query)

    # 2. Фильтрация по категории
    if cat_id:
        podcasts_list = podcasts_list.filter(category_id=cat_id)

    # 3. Пагинация (10 подкастов на страницу)
    paginator = Paginator(podcasts_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'indexer/index.html', {
        'podcasts': page_obj, # Теперь передаем объект страницы
        'categories': Category.objects.all(),
        'query': query,
        'cat_id': cat_id
    })

@login_required(login_url='/accounts/login/')  # Пока что отправляем неавторизованных в админку
def add_podcast(request):
    if request.method == 'POST':
        form = PodcastForm(request.POST)
        if form.is_valid():
            podcast = form.save(commit=False)
            podcast.uploader = request.user
            podcast.save()
            return redirect('index')
    else:
        form = PodcastForm()
    return render(request, 'indexer/add_podcast.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # Используем нашу новую форму
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def podcast_detail(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)
    comments = podcast.comments.all().order_by('-created_at') # Получаем все комментарии
    average_rating = podcast.get_average_rating() # Получаем среднюю оценку

    if request.method == 'POST':
        # Если гость пытается отправить форму, кидаем его на логин
        if not request.user.is_authenticated:
            return redirect('login')
            
        # Если юзер нажал кнопку отправки комментария
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.podcast = podcast
                comment.user = request.user
                comment.save()
                return redirect('podcast_detail', podcast_id=podcast.id)
                
        # Если юзер нажал кнопку отправки оценки
        elif 'rating_submit' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                # update_or_create обновляет оценку, если юзер уже голосовал, или создает новую
                Rating.objects.update_or_create(
                    podcast=podcast,
                    user=request.user,
                    defaults={'score': rating_form.cleaned_data['score']}
                )
                return redirect('podcast_detail', podcast_id=podcast.id)

    # Если это просто переход на страницу (GET запрос)
    comment_form = CommentForm()
    rating_form = RatingForm()

    # Если юзер авторизован, проверим, ставил ли он уже оценку, чтобы показать её в выпадающем списке
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(podcast=podcast, user=request.user).first()
        if user_rating:
            rating_form = RatingForm(instance=user_rating)

    return render(request, 'indexer/podcast_detail.html', {
        'podcast': podcast,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'average_rating': average_rating,
    })
# --- ЛИЧНЫЙ КАБИНЕТ И ПРАВА ---

@login_required(login_url='/accounts/login/')
def profile(request):
    user_podcasts = Podcast.objects.filter(uploader=request.user).order_by('-created_at')
    favorite_podcasts = request.user.favorite_podcasts.all()
    
    return render(request, 'indexer/profile.html', {
        'user_podcasts': user_podcasts,
        'favorite_podcasts': favorite_podcasts
    })

@login_required(login_url='/accounts/login/')
def edit_podcast(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)
    
    if podcast.uploader != request.user:
        return HttpResponseForbidden("У вас нет прав для редактирования этого подкаста.")
        
    if request.method == 'POST':
        form = PodcastForm(request.POST, instance=podcast)
        if form.is_valid():
            form.save()
            return redirect('podcast_detail', podcast_id=podcast.id)
    else:
        form = PodcastForm(instance=podcast)
        
    return render(request, 'indexer/edit_podcast.html', {'form': form, 'podcast': podcast})

@login_required(login_url='/accounts/login/')
def delete_podcast(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)
    
    if podcast.uploader != request.user:
        return HttpResponseForbidden("У вас нет прав для удаления этого подкаста.")
        
    if request.method == 'POST':
        podcast.delete()
        return redirect('profile')
        
    return render(request, 'indexer/confirm_delete.html', {'podcast': podcast})

@login_required(login_url='/accounts/login/')
def toggle_favorite(request, podcast_id):
    podcast = get_object_or_404(Podcast, id=podcast_id)
    
    if request.user in podcast.favorites.all():
        podcast.favorites.remove(request.user)
    else:
        podcast.favorites.add(request.user)
        
    return redirect('podcast_detail', podcast_id=podcast.id)

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    if request.method == 'POST':
        # Передаем данные из формы сразу в две модели: базового юзера и его профиль
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile') # После сохранения кидаем обратно в кабинет
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)
        
    return render(request, 'indexer/edit_profile.html', {'u_form': u_form, 'p_form': p_form})

# --- ФОРУМ ---
def forum_list(request):
    topics = ForumTopic.objects.all().order_by('-created_at') # Достаем все темы
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ForumTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.author = request.user
            topic.save()
            return redirect('forum_list')
    else:
        form = ForumTopicForm()
        
    return render(request, 'indexer/forum.html', {'topics': topics, 'form': form})

def forum_topic(request, topic_id):
    topic = get_object_or_404(ForumTopic, id=topic_id)
    replies = topic.replies.all().order_by('created_at') # Достаем ответы к теме
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ForumReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.topic = topic
            reply.save()
            return redirect('forum_topic', topic_id=topic.id)
    else:
        form = ForumReplyForm()
        
    return render(request, 'indexer/forum_topic.html', {'topic': topic, 'replies': replies, 'form': form})