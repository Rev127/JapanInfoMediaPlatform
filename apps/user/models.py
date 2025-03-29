from django.db import models
from apps.mediaProducts.models import PublicationUnit
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class GroupProxy(Group):
    class Meta:
        proxy = True
        auto_created = True
        verbose_name = 'group_proxy'
        verbose_name_plural = "groups_proxy"


class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='users/', blank=True, null=True, verbose_name='Аватар')

    groups = models.ManyToManyField(
        Group,
        related_name="profile_groups",  # Custom related_name to avoid conflicts
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="profile_permissions",  # Custom related_name to avoid conflicts
        blank=True
    )

class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Користувач')
    publication_unit = models.ForeignKey(PublicationUnit, on_delete=models.CASCADE, verbose_name='Публікація')
    content = models.TextField(max_length=255, verbose_name='Коментар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')

    def __str__(self):
        return self.content