from django.test import SimpleTestCase
from django.urls import reverse, resolve
from apps.mediaProducts.views import work_view, publication_view, publication_unit_view

class MediaProductsURLsTestCase(SimpleTestCase):
    def test_work_url_resolves(self):
        url = reverse('work', args=['test-link'])
        self.assertEqual(resolve(url).func, work_view)

    def test_publication_url_resolves(self):
        url = reverse('publication', args=['manga', 'test-link'])
        self.assertEqual(resolve(url).func, publication_view)

    def test_publication_unit_url_resolves(self):
        url = reverse('publication_unit', args=['volume', 'test-link'])
        self.assertEqual(resolve(url).func, publication_unit_view)
