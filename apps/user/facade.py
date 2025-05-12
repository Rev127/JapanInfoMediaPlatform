from .models import Profile, Comment
from django.core.files.storage import default_storage
from django.conf import settings
import os

class UserViewer:
    @staticmethod
    def get_user_by_id(user_id):
        """Повертає користувача за ID"""
        try:
            return Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def update_profile(action, update_value, user):
        """Оновлює профіль користувача"""
        if action == 'username_update':
            if update_value and update_value != user.username:
                if not Profile.objects.filter(username=update_value).exists():
                    user.username = update_value
                    user.save()
                    return True
                else:
                    return False

        elif action == 'email_update':
            if update_value and update_value != user.email:
                if not Profile.objects.filter(email=update_value).exists():
                    user.email = update_value
                    user.save()
                    return True
                else:
                    return False

        elif action == 'avatar_update':
            if update_value:
                # Видалення старої аватарки
                if user.avatar:
                    old_avatar_path = os.path.join(settings.MEDIA_ROOT, user.avatar.name)
                    if os.path.exists(old_avatar_path):
                        os.remove(old_avatar_path)

                # Збереження нової аватарки
                avatar_name = default_storage.save(f"user_avatar/{user.username}_avatar_{update_value.name}", update_value)
                user.avatar = avatar_name
                user.save()
                return True

        return False

    @staticmethod
    def get_comments_by_publication_unit(publication_unit_id):
        """Повертає коментарі до публікаційної одиниці"""
        return Comment.objects.filter(publication_unit_id=publication_unit_id)