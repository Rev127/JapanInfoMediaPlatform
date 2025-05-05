from .models import Work, Characters

class MediaProductsViewer:
    @staticmethod
    def get_work_info(work_id):
        """Повертає інформацію про твір за ID"""
        try:
            return Work.objects.prefetch_related('genre').select_related('author').get(id=work_id)
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publication_by_work(work_id):
        """Повертає публікації, пов'язані з твором"""
        try:
            manga = Work.objects.get(id=work_id).manga_publications.all()
            anime = Work.objects.get(id=work_id).anime_publications.all()
            novel = Work.objects.get(id=work_id).novel_publications.all()
            return {
                'manga': manga,
                'anime': anime,
                'novel': novel
            }
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publication_unit_by_publication(publication):
        """Повертає публікаційні одиниці, пов'язані з публікацією"""
        try:
            return publication.publication_unit.all()
        except Exception as e:
            return None


    @staticmethod
    def get_active_characters_by_publication_unit(publication_unit_id):
        """Повертає активних персонажів за ID публікаційної одиниці"""
        try:
            return Characters.objects.filter(character_publications__publication_unit_id=publication_unit_id)
        except Characters.DoesNotExist:
            return None
