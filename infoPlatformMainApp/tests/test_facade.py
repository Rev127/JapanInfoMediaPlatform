import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infoPlatform.settings")
django.setup()

from django.test import TestCase
from infoPlatformMainApp.models import ServerNews, WorkNews
from apps.user.models import Profile
from infoPlatformMainApp.facade import NewsViewer

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = Profile.objects.create(username="testuser", password="password")
        self.server_news = ServerNews.objects.create(
            content="The server will be down for maintenance on 2023-10-01.",
            news_type="INFO",
            user=self.user
        )
        self.work_news = WorkNews.objects.create(
            title="New Volume Release",
            content="The new volume of your favorite manga is out!",
            user=self.user
        )

    def test_get_server_news(self):
        retrieved_news = NewsViewer.get_server_news()
        self.assertEqual(retrieved_news.first(), self.server_news)

    def test_get_work_news(self):
        retrieved_news = NewsViewer.get_work_news()
        self.assertEqual(retrieved_news.first(), self.work_news)