from django.db.models import Count, Q

from .models import Category, Tag


# procesador de contexto: categorías y etiquetas disponibles en todas las plantillas
def catalog_filters(request):
    available = Q(products__available=True)
    return {
        'nav_categories': Category.objects.annotate(total=Count('products', filter=available)).filter(total__gt=0),
        'nav_tags': Tag.objects.annotate(total=Count('products', filter=available)).filter(total__gt=0),
    }
