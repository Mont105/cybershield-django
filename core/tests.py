from django.test import TestCase
from django.urls import reverse


class CoreViewTests(TestCase):
    def test_inicio_responde(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_pagina_404_personalizada(self):
        response = self.client.get('/esta-ruta-no-existe/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
