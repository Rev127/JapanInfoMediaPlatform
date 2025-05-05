from .models import Profile, Comment

class UserViewer:
    @staticmethod
    def get_user_by_id(user_id):
        """Повертає користувача за ID"""
        try:
            return Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def get_comments_by_publication_unit(publication_unit_id):
        """Повертає коментарі до публікаційної одиниці"""
        try:
            return Comment.objects.filter(publication_unit_id=publication_unit_id)
        except Comment.DoesNotExist:
            return []