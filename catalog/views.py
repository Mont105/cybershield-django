from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category, Product, Tag


# controlador del catálogo con filtros por GET
def catalog_view(request):
    products_list = (
        Product.objects.filter(available=True)
        .select_related('category')
        .prefetch_related('tags')
    )

    active_category = None
    active_tag = None

    # filtro por categoría (404 si no existe)
    category_slug = request.GET.get('categoria')
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products_list = products_list.filter(category=active_category)

    # filtro por etiqueta (404 si no existe)
    tag_slug = request.GET.get('etiqueta')
    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        products_list = products_list.filter(tags=active_tag)

    # paginación de 5 elementos
    paginator = Paginator(products_list, 5)
    page_obj = paginator.get_page(request.GET.get('page'))

    # conserva los filtros al cambiar de página
    filters = request.GET.copy()
    filters.pop('page', None)

    return render(request, 'catalog/catalog.html', {
        'page_obj': page_obj,
        'active_category': active_category,
        'active_tag': active_tag,
        'filter_query': filters.urlencode(),
    })


# controlador del detalle de un servicio
def product_detail_view(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('tags'),
        pk=pk,
        available=True,
    )
    return render(request, 'catalog/detail.html', {'product': product})
