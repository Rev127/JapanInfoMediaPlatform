from ckeditor.fields import RichTextField
from django.db import models
from slugify import slugify
from django.core.exceptions import ValidationError

# Create your models here.

class Work(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True, verbose_name='Опис')
    image = models.ImageField(upload_to='works/', blank=True, null=True, verbose_name='Зображення')
    genre = models.ManyToManyField('Genre', related_name='works', verbose_name='Жанр')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='works', verbose_name='Автор')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')

    def __str__(self):
        return self.get_title()

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

    def get_genres(self):
        return self.genre.all()

    def get_author(self):
        return self.author

    def get_description(self):
        return self.description

    def get_image(self):
        return self.image.url if self.image else None

    def get_title(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')

    def __str__(self):
        return self.get_name()

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ім\'я')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')
    work_years = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Роки творчості')

    def __str__(self):
        return self.get_name()

    def get_description(self):
        return self.description

    def get_name(self):
        return self.name

    def get_work_years(self):
        return self.work_years

class Publication(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    cover_image = models.ImageField(upload_to='publications/', blank=True, null=True, verbose_name='Обкладинка')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='%(class)s_publications', verbose_name='Твір')
    publication_unit = models.ManyToManyField('PublicationUnit', blank=True, related_name='%(class)s_publications', verbose_name='Публікаційна одиниця')

    class Meta:
        abstract = True

    def __str__(self):
        return self.get_title()

    def get_title(self):
        return self.title

    def get_cover_image(self):
        return self.cover_image.url if self.cover_image else None

    def get_publication_unit(self):
        return self.publication_unit.all()

    def get_work(self):
        return self.work

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)


class Manga(Publication):
    artist = models.CharField(max_length=50, blank=True, null=True, verbose_name='Художник')
    publisher = models.CharField(max_length=50, blank=True, null=True, verbose_name='Видавництво')

    def clean(self):
        super().clean()

        if not self.pk:
            return
        # Перевірка, чи всі одиниці публікації є томами (Volumes)
        for unit in self.publication_unit.all():
            if not isinstance(unit, Volumes):
                raise ValidationError(f"Publication unit '{unit}' is not a volume and cannot be linked to Manga.")
            # Перевірка, чи одиниця публікації вже прив'язана до іншої публікації
            if Manga.objects.filter(publication_unit=unit).exclude(id=self.id).exists():
                raise ValidationError(f"Publication unit '{unit}' is already linked to another Manga.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_artist(self):
        return self.artist

    def get_publisher(self):
        return self.publisher

class Novel(Publication):
    illustrator = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ілюстратор')
    publisher = models.CharField(max_length=50, blank=True, null=True, verbose_name='Видавництво')

    def clean(self):
        super().clean()

        if not self.pk:
            return
        # Перевірка, чи всі одиниці публікації є томами (Volumes)
        for unit in self.publication_unit.all():
            if not isinstance(unit, Volumes):
                raise ValidationError(f"Publication unit '{unit}' is not a volume and cannot be linked to Novel.")
            # Перевірка, чи одиниця публікації вже прив'язана до іншої публікації
            if Novel.objects.filter(publication_unit=unit).exclude(id=self.id).exists():
                raise ValidationError(f"Publication unit '{unit}' is already linked to another Novel.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_illustrator(self):
        return self.illustrator

    def get_publisher(self):
        return self.publisher

class Anime(Publication):
    director = models.CharField(max_length=50, blank=True, null=True, verbose_name='Режисер')
    studio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Студія')

    def clean(self):
        super().clean()

        if not self.pk:
            return
        # Перевірка, чи всі одиниці публікації є сезонами (Seasons)
        for unit in self.publication_unit.all():
            if not isinstance(unit, Seasons):
                raise ValidationError(f"Publication unit '{unit}' is not a season and cannot be linked to Anime.")
            # Перевірка, чи одиниця публікації вже прив'язана до іншої публікації
            if Anime.objects.filter(publication_unit=unit).exclude(id=self.id).exists():
                raise ValidationError(f"Publication unit '{unit}' is already linked to another Anime.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def get_director(self):
        return self.director

    def get_studio(self):
        return self.studio

class PublicationUnit(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    description = RichTextField(blank=True, null=True, verbose_name='Опис')
    title_image = models.ImageField(upload_to='publication_units/', blank=True, null=True, verbose_name='Зображення')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')
    year_of_release = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Рік випуску')
    number = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Номер')
    active_characters = models.ManyToManyField('Characters', related_name='active_characters', verbose_name='Активні персонажі')
    last_update = models.DateTimeField(auto_now=True, verbose_name='Останнє оновлення')

    class Status(models.TextChoices):
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'
        Announced = 'announced', 'Announced'
        Suspended = 'suspended', 'Suspended'

    status = models.CharField(max_length=50, choices=Status.choices, verbose_name='Статус')

    def __str__(self):
        return self.get_title()

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_title_image(self):
        return self.title_image.url if self.title_image else None

    def get_year_of_release(self):
        return self.year_of_release

    def get_number(self):
        return self.number

    def get_active_characters(self):
        return self.active_characters.all()

    def get_status(self):
        return self.status

# Removed the get_publication method as it references an undefined attribute.

    def get_last_update(self):
        return self.last_update

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

class Volumes(PublicationUnit):
    chapter_count = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Кількість глав')

    def get_chapter_count(self):
        return self.chapter_count

    def __str__(self):
        return f"{self.get_title()} (Том №{self.get_number()})"

class Seasons(PublicationUnit):
    episode_count = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Кількість серій')

    def get_episode_count(self):
        return self.episode_count

    def __str__(self):
        return f"{self.get_title()} (Сезон №{self.get_number()})"

class Characters(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ім\'я')
    image = models.ImageField(upload_to='characters/', blank=True, null=True, verbose_name='Зображення')

    def __str__(self):
        # Отримуємо всі PublicationUnit, де цей персонаж є активним
        publication_units = self.active_characters.all()

        # Збираємо унікальні назви робіт
        work_titles = set()
        for pub_unit in publication_units:
            if hasattr(pub_unit, 'manga_publications'):
                for manga in pub_unit.manga_publications.all():
                    work_titles.add(manga.work.title)
            if hasattr(pub_unit, 'novel_publications'):
                for novel in pub_unit.novel_publications.all():
                    work_titles.add(novel.work.title)
            if hasattr(pub_unit, 'anime_publications'):
                for anime in pub_unit.anime_publications.all():
                    work_titles.add(anime.work.title)

        if work_titles:
            return f"{self.name} ({', '.join(work_titles)})"
        return self.name

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image.url if self.image else None

    def get_character_publications(self):
        return self.character_publications.all()

class CharacterPublication(models.Model):
    character = models.ForeignKey('Characters', on_delete=models.CASCADE, related_name='character_publications')
    description = RichTextField(blank=True, null=True, verbose_name='Опис')

    class PublicationType(models.TextChoices):
        Manga = 'manga', 'Manga'
        Novel = 'novel', 'Novel'
        Anime = 'anime', 'Anime'

    publication_type = models.CharField(max_length=50, choices=PublicationType.choices, verbose_name='Тип роботи')

    def clean(self):
        # Перевірка, чи вже існує CharacterPublication з таким типом для цього персонажа
        if CharacterPublication.objects.filter(character=self.character, publication_type=self.publication_type).exists():
            raise ValidationError(f"CharacterPublication with type '{self.publication_type}' already exists for this character.")

    def save(self, *args, **kwargs):
        # Виклик clean перед збереженням
        self.clean()
        super().save(*args, **kwargs)

    def get_description(self):
        return self.description

    def get_publication_type(self):
        return self.publication_type

    def get_character(self):
        return self.character

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['character', 'publication_type'], name='unique_character_publication_type')
        ]
