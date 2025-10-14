from django.test import TestCase
from apps.user.facade import UserViewer
from apps.user.models import Profile, Comment
from apps.mediaProducts.models import Volumes

class UserViewerTestCase(TestCase):
    def setUp(self):
        self.user = Profile.objects.create(username="testuser", password="password")
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.comment = Comment.objects.create(
            user=self.user,
            content="This is a test comment",
            publication_unit=self.volume
        )

    def test_get_user_by_id(self):
        retrieved_user = UserViewer.get_user_by_id(self.user.id)
        self.assertEqual(retrieved_user, self.user)

    def test_get_comments_by_publication_unit(self):
        comments = UserViewer.get_comments_by_publication_unit(self.volume.id)
        self.assertEqual(self.comment, comments.first())

    def test_add_comment(self):
        new_comment = UserViewer.add_comment(self.user, self.volume, "Another test comment")
        self.assertEqual(new_comment.content, "Another test comment")
        self.assertEqual(new_comment.user, self.user)
        self.assertEqual(new_comment.publication_unit, self.volume)

    def test_update_profile_username(self):
        result = UserViewer.update_profile('username_update', 'newusername', self.user)
        self.assertTrue(result)
        self.assertEqual(self.user.username, 'newusername')