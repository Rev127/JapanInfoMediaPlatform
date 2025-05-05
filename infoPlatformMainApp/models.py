from django.db import models
from slugify import slugify
from apps.user.models import Profile

# Create your models here.
class BasicNews(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Користувач')
    content = models.TextField(max_length=255, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def __str__(self):
        return self.title

    def get_user(self):
        return self.user

    def get_content(self):
        return self.content

    def get_created_at(self):
        return self.created_at

    class Meta:
        abstract = True

class ServerNews(BasicNews):
    class NewsType(models.TextChoices):
        INFO = 'INFO', 'Інформація'
        WARNING = 'WARNING', 'Попередження'
        ERROR = 'ERROR', 'Помилка'
        Update = 'Update', 'Оновлення'

    news_type = models.CharField(max_length=20, choices=NewsType.choices, default=NewsType.INFO, verbose_name='Тип новини')

    def get_news_type(self):
        return self.news_type

class WorkNews(BasicNews):
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Зображення')
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name='Посилання')
    title = models.CharField(max_length=255, verbose_name='Заголовок')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.link:
            self.link = slugify(self.title, to_lower=True)
        super().save(*args, **kwargs)

    def get_image(self):
        return self.image.url if self.image else None

    def get_title(self):
        return self.title

