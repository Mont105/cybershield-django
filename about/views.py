from django.shortcuts import render

# controlador de la página nosotros
def about_view(request):
    return render(request, 'about/about.html')

