import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infoPlatform.settings")
django.setup()

from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.mediaProducts.models import Work, Author, Manga, Anime, Novel, Volumes, Seasons, Characters, CharacterPublication

class ModelsTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author", work_years=5)
        self.work = Work.objects.create(title="Test Work", author=self.author)
        self.volume = Volumes.objects.create(title="Volume 1", number=1)
        self.season = Seasons.objects.create(title="Season 1", number=1)
        self.character = Characters.objects.create(name="Test Character")

    def test_work_creation(self):
        self.assertEqual(self.work.get_title(), "Test Work")
        self.assertEqual(self.work.get_author(), self.author)

    def test_manga_creation(self):
        manga = Manga.objects.create(title="Test Manga", artist="Test Artist", publisher="Test Publisher", work=self.work)
        self.assertEqual(manga.get_title(), "Test Manga")
        self.assertEqual(manga.get_artist(), "Test Artist")
        self.assertEqual(manga.get_publisher(), "Test Publisher")
        self.assertEqual(manga.get_work(), self.work)

    def test_manga_publication_unit_validation(self):
        manga = Manga.objects.create(title="Test Manga", artist="Test Artist", publisher="Test Publisher", work=self.work)

        manga.publication_unit.add(self.volume)
        manga.publication_unit.add(self.season)

        with self.assertRaises(ValidationError):
            manga.full_clean()

    def test_anime_creation(self):
        anime = Anime.objects.create(title="Test Anime", studio="Test Studio", director="Test Director", work=self.work)
        self.assertEqual(anime.get_title(), "Test Anime")
        self.assertEqual(anime.get_studio(), "Test Studio")
        self.assertEqual(anime.get_director(), "Test Director")
        self.assertEqual(anime.get_work(), self.work)

    def test_anime_publication_unit_validation(self):
        anime = Anime.objects.create(title="Test Anime", studio="Test Studio", director="Test Director", work=self.work)

        anime.publication_unit.add(self.volume)
        anime.publication_unit.add(self.season)

        with self.assertRaises(ValidationError):
            anime.full_clean()

    def test_novel_creation(self):
        novel = Novel.objects.create(title="Test Novel", illustrator="Test Illustrator", publisher="Test Publisher", work=self.work)
        self.assertEqual(novel.get_title(), "Test Novel")
        self.assertEqual(novel.get_illustrator(), "Test Illustrator")
        self.assertEqual(novel.get_publisher(), "Test Publisher")
        self.assertEqual(novel.get_work(), self.work)

    def test_novel_publication_unit_validation(self):
        novel = Novel.objects.create(title="Test Novel", illustrator="Test Illustrator", publisher="Test Publisher", work=self.work)

        novel.publication_unit.add(self.volume)
        novel.publication_unit.add(self.season)

        with self.assertRaises(ValidationError):
            novel.full_clean()

    def test_volumes_creation(self):
        volume = Volumes.objects.create(title="Volume 1", number=1)
        self.assertEqual(volume.get_title(), "Volume 1")
        self.assertEqual(volume.get_number(), 1)

    def test_seasons_creation(self):
        season = Seasons.objects.create(title="Season 1", number=1)
        self.assertEqual(season.get_title(), "Season 1")
        self.assertEqual(season.get_number(), 1)

    def test_characters_creation(self):
        character = Characters.objects.create(name="Test Character")
        self.assertEqual(character.get_name(), "Test Character")

    def test_character_publication_creation(self):
        character_publication = CharacterPublication.objects.create(character=self.character, publication_type='manga')
        self.assertEqual(character_publication.get_character(), self.character)
        self.assertEqual(character_publication.get_publication_type(), 'manga')

    def test_character_publication_validation(self):
        CharacterPublication.objects.create(character=self.character, publication_type='manga')
        with self.assertRaises(ValidationError):
            character_publication = CharacterPublication(character=self.character, publication_type='manga')
            character_publication.full_clean()





