from django.urls import path
from . import views

# rutas de inicio
urlpatterns = [
    path('', views.home_view, name='home'),
]
