from django.urls import path
from . import views

# rutas de nosotros
urlpatterns = [
    path('', views.about_view, name='about'),
]
