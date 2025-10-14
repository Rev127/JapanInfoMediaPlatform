from django.test import TestCase, Client
from django.urls import reverse
from apps.mediaProducts.models import Work, Author, Manga, Anime, Novel, Volumes
from apps.user.models import Profile
from apps.user.facade import UserViewer

class MediaProductsViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Test Author", work_years=5)
        self.work = Work.objects.create(title="Test Work", author=self.author)
        self.manga = Manga.objects.create(title="Test Manga", work=self.work)
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.manga.publication_unit.add(self.volume)
        self.user = Profile.objects.create(username="testuser", password="password")
        self.client.force_login(self.user)

    def test_work_view_get(self):
        response = self.client.get(reverse('work', args=[self.work.link]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.work.title)

    def test_work_view_post_track(self):
        response = self.client.post(reverse('work', args=[self.work.link]), {'action': 'track'})
        self.assertEqual(response.status_code, 302)  # Redirect after tracking
        self.assertTrue(self.user.tracking_works.filter(id=self.work.id).exists())

    def test_work_view_post_untrack(self):
        self.user.tracking_works.add(self.work)
        response = self.client.post(reverse('work', args=[self.work.link]), {'action': 'untrack'})
        self.assertEqual(response.status_code, 302)  # Redirect after untracking
        self.assertFalse(self.user.tracking_works.filter(id=self.work.id).exists())


    def test_publication_view_get(self):
        response = self.client.get(reverse('publication', args=['manga', self.manga.link]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.manga.title)


    def test_publication_unit_view_get(self):
        response = self.client.get(reverse('publication_unit', args=['volume', self.volume.link]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.volume.title)

    def test_publication_unit_view_post_add_comment(self):
        response = self.client.post(reverse('publication_unit', args=['volume', self.volume.link]), {
            'action': 'add_comment',
            'comment': 'Test Comment'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after adding comment
        self.assertTrue(UserViewer.get_comments_by_publication_unit(self.volume.id).exists())