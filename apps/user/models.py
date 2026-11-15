from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from apps.mediaProducts.models import PublicationUnit, Work
from django.contrib.auth.models import AbstractUser, Group, Permission
from filebrowser.fields import FileBrowseField

# Create your models here.
class Profile(AbstractUser):
    avatar = FileBrowseField(verbose_name='Аватар', max_length=255,
                             directory='user_avatar/', extensions=['.jpg', '.jpeg', '.png'], blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name="user_profiles",
                                    blank=True, verbose_name='Групи')
    user_permissions = models.ManyToManyField(Permission, related_name="user_permissions_set",
                                              blank=True, verbose_name='Дозволи')
    tracking_works = models.ManyToManyField(Work, through="TrackedWork", verbose_name="Відстежувані твори",
                                            blank=True, related_name='tracking_works')

    def get_tracking_works(self):
        return self.tracking_works.all()

    def get_avatar(self):
        return self.avatar.url if self.avatar else None

    def work_is_tracked(self, work):
        return self.tracking_works.filter(id=work.id).exists()

    def __str__(self):
        return self.username

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Користувач')
    publication_unit = models.ForeignKey(PublicationUnit, on_delete=models.CASCADE, verbose_name='Публікаційна одиниця')
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

    class TrackedWork(models.Model):
        user = models.ForeignKey(
            Profile,
            on_delete=models.CASCADE,
            related_name="tracked_entries"
        )

        work = models.ForeignKey(
            Work,
            on_delete=models.CASCADE,
            related_name="tracked_entries"
        )

        rating = models.PositiveSmallIntegerField(
            null=True,
            blank=True,
            validators=[
                MinValueValidator(1),
                MaxValueValidator(10)
            ]
        )

        class Meta:
            constraints = [
                models.UniqueConstraint(
                    fields=["user", "work"],
                    name="unique_tracked_work"
                )
            ]