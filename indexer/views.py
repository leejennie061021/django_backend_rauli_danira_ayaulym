from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Podcast
from .forms import PodcastForm

def index(request):
    podcasts = Podcast.objects.all().order_by('-created_at')
    return render(request, 'indexer/index.html', {'podcasts': podcasts})

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматически логиним после регистрации
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def podcast_detail(request, podcast_id):
    # Ищем подкаст по ID. Если его нет — выдаст ошибку 404 (Страница не найдена)
    podcast = get_object_or_404(Podcast, id=podcast_id) 
    return render(request, 'indexer/podcast_detail.html', {'podcast': podcast})