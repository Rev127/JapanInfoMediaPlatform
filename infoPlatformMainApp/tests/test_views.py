from django.test import TestCase, Client
from django.urls import reverse
from apps.mediaProducts.models import Work, Author

class InfoPlatformMainAppViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Test Author", work_years=5)
        self.work = Work.objects.create(title="Test Work", link="test-link", author=self.author)

    def test_index_view_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mainapp/index.html')
        self.assertIn('server_news', response.context)
        self.assertIn('work_news', response.context)
        self.assertIn('last_update_works', response.context)
        self.assertIn('user', response.context)

    def test_ajax_search_view_get_with_query(self):
        response = self.client.get(reverse('search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], [{'title': self.work.title, 'link': self.work.link}])

    def test_ajax_search_view_get_without_query(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['results'], [])