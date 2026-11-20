from django.urls import path
from . import views

# rutas del catálogo
urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
]
