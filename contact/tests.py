from django.test import TestCase
from django.urls import reverse

from .forms import ContactForm

DATOS_VALIDOS = {
    'name': 'Roberto Fuentes',
    'email': 'rfuentes@empresa.com',
    'phone': '+56 9 1234 5678',
    'company': 'Empresa SpA',
    'service_type': 'ofensivo',
    'message': 'Necesitamos evaluar la seguridad de nuestra aplicación web.',
    'accept_terms': True,
}


class ContactFormTests(TestCase):
    def formulario(self, **cambios):
        return ContactForm({**DATOS_VALIDOS, **cambios})

    def test_acepta_datos_validos(self):
        self.assertTrue(self.formulario().is_valid())

    def test_rechaza_correo_gratuito(self):
        form = self.formulario(email='ana@gmail.com')
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_exige_nombre_y_apellido(self):
        form = self.formulario(name='Roberto')
        self.assertIn('name', form.errors)

    def test_rechaza_celular_invalido(self):
        form = self.formulario(phone='12345')
        self.assertIn('phone', form.errors)

    def test_normaliza_el_celular(self):
        form = self.formulario()
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone'], '+56912345678')

    def test_otro_servicio_pide_mensaje_mas_largo(self):
        form = self.formulario(service_type='otro', message='Mensaje de unos veinticinco caracteres.')
        self.assertIn('message', form.errors)

    def test_exige_aceptar_los_terminos(self):
        form = self.formulario(accept_terms=False)
        self.assertIn('accept_terms', form.errors)


class ContactViewTests(TestCase):
    def test_muestra_el_formulario(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_envio_valido_redirige(self):
        response = self.client.post(reverse('contact'), DATOS_VALIDOS)
        self.assertRedirects(response, reverse('contact'))

    def test_envio_invalido_vuelve_al_formulario(self):
        response = self.client.post(reverse('contact'), {**DATOS_VALIDOS, 'email': 'ana@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
