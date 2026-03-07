from .models import Category

def category_menu(request):
    return {
        'menu_categories': Category.objects.all()
    }