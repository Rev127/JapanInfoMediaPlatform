from django.db import models
from slugify import slugify


# Create your models here.

class Work(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')
    image = models.ImageField(upload_to='works/', blank=True, null=True, verbose_name='Зображення')
    genre = models.ManyToManyField('Genre', related_name='works')
    author = models.ForeignKey('Author', on_delete=models.CASCADE, related_name='works')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

class Genre(models.Model):
    name = models.CharField(max_length=50, verbose_name='Назва')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ім\'я')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')
    work_years = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Роки творчості')

    def __str__(self):
        return self.name

class Publication(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    cover_image = models.ImageField(upload_to='publications/', blank=True, null=True, verbose_name='Обкладинка')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='%(class)s_publications')

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

class Manga(Publication):
    artist = models.CharField(max_length=50, blank=True, null=True, verbose_name='Художник')


class Novel(Publication):
    illustrator = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ілюстратор')
    publisher = models.CharField(max_length=50, blank=True, null=True, verbose_name='Видавництво')


class Anime(Publication):
    director = models.CharField(max_length=50, blank=True, null=True, verbose_name='Режисер')
    studio = models.CharField(max_length=50, blank=True, null=True, verbose_name='Студія')


class MangaVolumes(models.Model):
    manga = models.ForeignKey('Manga', on_delete=models.CASCADE, related_name='volumes')
    publication_unit = models.ForeignKey('Volumes', on_delete=models.CASCADE, related_name='manga')

class NovelVolumes(models.Model):
    novel = models.ForeignKey('Novel', on_delete=models.CASCADE, related_name='volumes')
    publication_unit = models.ForeignKey('Volumes', on_delete=models.CASCADE, related_name='novel')

class AnimeSeasons(models.Model):
    anime = models.ForeignKey('Anime', on_delete=models.CASCADE, related_name='seasons')
    publication_unit = models.ForeignKey('Seasons', on_delete=models.CASCADE, related_name='anime')

class PublicationUnit(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')
    title_image = models.ImageField(upload_to='publication_units/', blank=True, null=True, verbose_name='Зображення')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')
    year_of_release = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Рік випуску')
    number = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Номер')

    class Status(models.TextChoices):
        ONGOING = 'ongoing', 'Ongoing'
        COMPLETED = 'completed', 'Completed'
        DROPPED = 'dropped', 'Dropped'
        Announced = 'announced', 'Announced'
        Suspended = 'suspended', 'Suspended'

    status = models.CharField(max_length=50, choices=Status.choices, verbose_name='Статус')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

class Volumes(PublicationUnit):
    chapter_count = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Кількість глав')

class Seasons(PublicationUnit):
    episode_count = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name='Кількість серій')

class ActiveCharacter(models.Model):
    character = models.ForeignKey('Characters', on_delete=models.CASCADE, related_name='active_works')
    publication_unit = models.ForeignKey('PublicationUnit', on_delete=models.CASCADE, related_name='characters')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')

class Characters(models.Model):
    name = models.CharField(max_length=50, verbose_name='Ім\'я')
    image = models.ImageField(upload_to='characters/', blank=True, null=True, verbose_name='Зображення')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.name, to_lower=True)
        super().save(*args, **kwargs)

class CharacterWork(models.Model):
    character = models.ForeignKey('Characters', on_delete=models.CASCADE, related_name='works')
    work = models.ForeignKey('Work', on_delete=models.CASCADE, related_name='characters')
    description = models.TextField(max_length=255, blank=True, null=True, verbose_name='Опис')

    class WorkType(models.TextChoices):
        Manga = 'manga', 'Manga'
        Novel = 'novel', 'Novel'
        Anime = 'anime', 'Anime'

    work_type = models.CharField(max_length=50, choices=WorkType.choices, verbose_name='Тип роботи')
