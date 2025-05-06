import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infoPlatform.settings")
django.setup()

from django.test import TestCase
from apps.user.models import Profile, Comment
from apps.mediaProducts.models import Volumes

class ModelTestCase(TestCase):
    def setUp(self):
        self.user = Profile.objects.create(username="testuser", password="password")
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.comment = Comment.objects.create(
            user=self.user,
            content="This is a test comment",
            publication_unit=self.volume
        )

    def test_profile(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.password, "password")
        self.assertIsNone(self.user.get_avatar())

    def test_comment(self):
        self.assertEqual(self.comment.get_content(), "This is a test comment")
        self.assertEqual(self.comment.get_user(), self.user)



