from django.db import models
from apps.mediaProducts.models import PublicationUnit, Work
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Аватар')

    groups = models.ManyToManyField(Group, related_name="user_profiles", blank=True, verbose_name='Групи')
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions_set", blank=True, verbose_name='Дозволи')
    tracking_works = models.ManyToManyField(Work, verbose_name="Відстежувані твори", blank=True, related_name='tracking_works')

    def get_tracking_works(self):
        return self.tracking_works.all()

    def get_avatar(self):
        return self.avatar.url if self.avatar else None


    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Користувач')
    publication_unit = models.ForeignKey(PublicationUnit, on_delete=models.CASCADE, verbose_name='Публікаціqна одиниця')
    content = models.TextField(max_length=255, verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def __str__(self):
        return self.content

    def get_user(self):
        return self.user

    def get_content(self):
        return self.content

    def get_created_at(self):
        return self.created_at