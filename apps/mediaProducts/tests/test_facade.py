import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infoPlatform.settings")
django.setup()

from django.test import TestCase
from apps.mediaProducts.facade import MediaProductsViewer
from apps.mediaProducts.models import Work, Author, Manga, Anime, Novel, Volumes

class MediaProductsViewerTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", work_years=5)
        self.work = Work.objects.create(title="Test Work", author=self.author)
        self.manga = Manga.objects.create(title="Test Manga", work=self.work)
        self.anime = Anime.objects.create(title="Test Anime", work=self.work)
        self.novel = Novel.objects.create(title="Test Novel", work=self.work)
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.manga.publication_unit.add(self.volume)

    def test_get_work_info(self):
        retrieved_work = MediaProductsViewer.get_work_info(self.work.id)
        self.assertEqual(retrieved_work, self.work)

    def test_get_publications_by_work(self):
        publications = MediaProductsViewer.get_publications_by_work(self.work.id)
        self.assertIn(self.manga, publications['manga'])
        self.assertIn(self.anime, publications['anime'])
        self.assertIn(self.novel, publications['novel'])

    def test_get_publication_by_type(self):
        retrieved_manga = MediaProductsViewer.get_publication_by_type('manga', self.work.id)
        self.assertIn(self.manga, retrieved_manga)

    def test_get_publication_units_by_publication(self):
        units = MediaProductsViewer.get_publication_units_by_publication(self.manga)
        self.assertEqual(self.volume.title, units.first().title)
        self.assertEqual(len(units), 1)

    def test_get_last_update_work(self):
        last_update_works = MediaProductsViewer.get_last_update_work()
        self.assertEqual(self.work, last_update_works.first())





