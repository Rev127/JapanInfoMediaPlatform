import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infoPlatform.settings")
django.setup()

from django.test import TestCase
from infoPlatformMainApp.models import ServerNews, WorkNews
from apps.user.models import Profile

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = Profile.objects.create(username="testuser", password="password")
        self.server_news = ServerNews.objects.create(
            content="The server will be down for maintenance.",
            news_type="INFO",
            user=self.user
        )
        self.work_news = WorkNews.objects.create(
            title="New Volume Release",
            content="The new volume of your favorite manga is out!",
            user=self.user
        )

    def test_server_news(self):
        self.assertEqual(self.server_news.get_content(), "The server will be down for maintenance.")
        self.assertEqual(self.server_news.get_news_type(), "INFO")
        self.assertEqual(self.server_news.get_user(), self.user)

    def test_work_news(self):
        self.assertEqual(self.work_news.get_title(), "New Volume Release")
        self.assertEqual(self.work_news.get_content(), "The new volume of your favorite manga is out!")
        self.assertEqual(self.work_news.get_user(), self.user)