from django.contrib import admin
from .models import Podcast, Category

admin.site.register(Podcast)
admin.site.register(Category)