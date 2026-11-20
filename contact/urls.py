from django.urls import path
from . import views

# rutas de contacto
urlpatterns = [
    path('', views.contact_view, name='contact'),
]
