from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import SERVICE_CHOICES, ContactForm


# controlador del formulario de contacto
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # envío válido: solo muestra confirmación
            name = form.cleaned_data['name']
            messages.success(request, f"Gracias {name}, recibimos su solicitud. Un especialista lo contactará en 24 horas.")
            return redirect('contact')
    else:
        # preselección del servicio desde el detalle
        servicio = request.GET.get('servicio')
        initial = {'service_type': servicio} if servicio in dict(SERVICE_CHOICES) else {}
        form = ContactForm(initial=initial)

    return render(request, 'contact/contact.html', {'form': form})
