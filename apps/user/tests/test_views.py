from django.test import TestCase, Client
from django.urls import reverse
from apps.user.models import Profile
from apps.user.facade import UserViewer

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Profile.objects.create(username="testuser", password="password")
        self.client.force_login(self.user)

    def test_profile_view_get(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/profile.html')

    def test_profile_view_post_avatar_update(self):
        response = self.client.post(reverse('profile'), {
            'action': 'username_update',
            'update_value': 'testuser_updated'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after update
        self.assertEqual(UserViewer.get_user_by_id(self.user.id).username, 'testuser_updated')

    def test_profile_view_post_invalid_action(self):
        response = self.client.post(reverse('profile'), {
            'action': 'invalid_action',
            'update_value': 'test_value'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after failure
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any(message.level_tag == 'error' for message in messages))