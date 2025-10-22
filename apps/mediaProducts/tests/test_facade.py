from django.test import TestCase
from apps.mediaProducts.facade import MediaProductsViewer
from apps.mediaProducts.models import Work, Author, Manga, Anime, Novel, Volumes
from apps.user.models import Profile


class MediaProductsViewerTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", work_years=5)
        self.work = Work.objects.create(title="Test Work", author=self.author)
        self.manga = Manga.objects.create(title="Test Manga", work=self.work)
        self.anime = Anime.objects.create(title="Test Anime", work=self.work)
        self.novel = Novel.objects.create(title="Test Novel", work=self.work)
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.user = Profile.objects.create(username="testuser", password="password")
        self.manga.publication_unit.add(self.volume)

    def test_get_work_info(self):
        retrieved_work = MediaProductsViewer.get_work_info(self.work.link)
        self.assertEqual(retrieved_work, self.work)

    def test_get_publications_by_work(self):
        publications = MediaProductsViewer.get_publications_by_work(self.work.link)
        self.assertIn(self.manga, publications['manga'])
        self.assertIn(self.anime, publications['anime'])
        self.assertIn(self.novel, publications['novel'])

    def test_get_publication_by_type(self):
        retrieved_manga = MediaProductsViewer.get_publication_by_type('manga', self.manga.link)
        self.assertEqual(self.manga, retrieved_manga)

    def test_get_publication_units_by_publication(self):
        units = MediaProductsViewer.get_publication_units_by_publication(self.manga)
        self.assertEqual(self.volume.title, units.first().title)
        self.assertEqual(len(units), 1)

    def test_get_last_update_work(self):
        last_update_works = MediaProductsViewer.get_last_update_work()
        self.assertEqual(self.work, last_update_works.first())

    def test_get_publication_unit_by_type_and_link(self):
        publication_unit_type = 'volume'
        publication_unit = MediaProductsViewer.get_publication_unit_by_type_and_link(publication_unit_type, self.volume.link)
        self.assertEqual(self.volume, publication_unit)

    def test_track_and_untrack_work(self):
        MediaProductsViewer.track_work(self.user, self.work)
        self.assertIn(self.work, self.user.tracking_works.all())
        MediaProductsViewer.untrack_work(self.user, self.work)
        self.assertEqual(self.user.tracking_works.count(), 0)

    def test_get_works_by_title_fragment(self):
        works = MediaProductsViewer.get_works_by_title_fragment("Test")
        self.assertIn(self.work, works)
        self.assertEqual(len(works), 1)






