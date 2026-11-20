from django.shortcuts import render


# controlador de la página de inicio
def home_view(request):
    return render(request, 'core/index.html')


# controlador de la página 404 personalizada
def error_404_view(request, exception):
    return render(request, '404.html', status=404)
