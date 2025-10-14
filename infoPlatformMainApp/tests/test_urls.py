from django.test import SimpleTestCase
from django.urls import reverse, resolve
from infoPlatformMainApp.views import index, ajax_search

class InfoPlatformMainAppURLsTestCase(SimpleTestCase):
    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, ajax_search)