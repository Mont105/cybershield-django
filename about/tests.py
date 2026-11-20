from django.test import TestCase
from django.urls import reverse


class AboutViewTests(TestCase):
    def test_pagina_nosotros_responde(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
