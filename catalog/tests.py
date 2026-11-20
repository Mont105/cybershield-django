from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Tag


class CatalogViewTests(TestCase):
    """El catálogo se llena con la migración inicial, por eso hay datos desde el primer momento."""

    def test_lista_servicios_disponibles(self):
        response = self.client.get(reverse('catalog'))
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['page_obj']), 0)

    def test_pagina_de_cinco_servicios(self):
        response = self.client.get(reverse('catalog'))
        self.assertLessEqual(len(response.context['page_obj']), 5)

    def test_filtra_por_categoria(self):
        categoria = Category.objects.first()
        response = self.client.get(reverse('catalog'), {'categoria': categoria.slug})
        self.assertEqual(response.status_code, 200)
        for producto in response.context['page_obj']:
            self.assertEqual(producto.category, categoria)

    def test_filtra_por_etiqueta(self):
        etiqueta = Tag.objects.first()
        response = self.client.get(reverse('catalog'), {'etiqueta': etiqueta.slug})
        self.assertEqual(response.status_code, 200)
        for producto in response.context['page_obj']:
            self.assertIn(etiqueta, producto.tags.all())

    def test_categoria_inexistente_devuelve_404(self):
        response = self.client.get(reverse('catalog'), {'categoria': 'no-existe'})
        self.assertEqual(response.status_code, 404)

    def test_etiqueta_inexistente_devuelve_404(self):
        response = self.client.get(reverse('catalog'), {'etiqueta': 'no-existe'})
        self.assertEqual(response.status_code, 404)

    def test_detalle_muestra_el_servicio(self):
        producto = Product.objects.filter(available=True).first()
        response = self.client.get(reverse('product_detail', args=[producto.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, producto.title)

    def test_servicio_no_disponible_devuelve_404(self):
        producto = Product.objects.first()
        producto.available = False
        producto.save()
        response = self.client.get(reverse('product_detail', args=[producto.pk]))
        self.assertEqual(response.status_code, 404)

    def test_servicio_no_disponible_no_sale_en_el_catalogo(self):
        producto = Product.objects.first()
        producto.available = False
        producto.save()
        response = self.client.get(reverse('catalog'))
        self.assertNotIn(producto, response.context['page_obj'])
