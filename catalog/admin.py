from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product, Tag

# personalización del panel de administración
admin.site.site_header = "CyberShield | Administración"
admin.site.site_title = "CyberShield Admin"
admin.site.index_title = "Panel de gestión del catálogo"


# servicios editables dentro de la categoría
class ProductInline(admin.TabularInline):
    model = Product
    fields = ('title', 'price', 'available')
    extra = 0
    show_change_link = True


# administración de categorías
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'total_products', 'created')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'updated')
    inlines = [ProductInline]

    @admin.display(description="N° de servicios")
    def total_products(self, obj):
        return obj.products.count()


# administración de etiquetas
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'total_products')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created', 'updated')

    @admin.display(description="N° de servicios")
    def total_products(self, obj):
        return obj.products.count()


# administración de productos / servicios
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # personalización del listado
    list_display = ('title', 'image_preview', 'category', 'price', 'available', 'tag_list', 'created')
    list_display_links = ('title',)
    list_editable = ('price', 'available')
    list_filter = ('available', 'category', 'tags', 'created')
    search_fields = ('title', 'description', 'category__name', 'tags__name')
    # personalización del formulario
    readonly_fields = ('created', 'updated', 'image_preview')
    ordering = ('category', 'title')
    date_hierarchy = 'created'
    list_per_page = 10
    filter_horizontal = ('tags',)
    fieldsets = (
        ('Información del servicio', {
            'fields': ('title', 'description', 'price', 'available'),
        }),
        ('Clasificación', {
            'fields': ('category', 'tags'),
        }),
        ('Imagen', {
            'fields': ('image', 'image_preview'),
        }),
        ('Auditoría', {
            'classes': ('collapse',),
            'fields': ('created', 'updated'),
        }),
    )
    # acciones masivas
    actions = ('mark_available', 'mark_unavailable')

    # columnas calculadas
    @admin.display(description="Imagen")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;border-radius:4px;">', obj.image.url)
        return "—"

    @admin.display(description="Etiquetas")
    def tag_list(self, obj):
        return ", ".join(tag.name for tag in obj.tags.all())

    @admin.action(description="Marcar seleccionados como disponibles")
    def mark_available(self, request, queryset):
        updated = queryset.update(available=True)
        self.message_user(request, f"{updated} servicio(s) marcados como disponibles.")

    @admin.action(description="Marcar seleccionados como no disponibles")
    def mark_unavailable(self, request, queryset):
        updated = queryset.update(available=False)
        self.message_user(request, f"{updated} servicio(s) marcados como no disponibles.")

    # optimización de consultas
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category').prefetch_related('tags')
