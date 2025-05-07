from .models import Work, Manga, Anime, Novel
from django.db.models import Max

class MediaProductsViewer:
    @staticmethod
    def get_work_info(work_id):
        """Повертає інформацію про твір за ID"""
        try:
            return Work.objects.prefetch_related('genre').select_related('author').get(id=work_id)
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_last_update_work():
        """Повертає список робіт, відсортованих за останнім оновленням"""
        try:
            return Work.objects.prefetch_related(
                'manga_publications__publication_unit',
                'anime_publications__publication_unit',
                'novel_publications__publication_unit'
            ).annotate(
                last_update=Max('manga_publications__publication_unit__last_update')
            ).order_by('-last_update')
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publications_by_work(work_id):
        """Повертає публікації, пов'язані з твором"""
        try:
            manga = Manga.objects.filter(work_id=work_id)
            anime = Anime.objects.filter(work_id=work_id)
            novel = Novel.objects.filter(work_id=work_id)
            return {
                'manga': manga,
                'anime': anime,
                'novel': novel
            }
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publication_by_type(publication_type, work_id):
        """Повертає публікації за типом"""
        try:
            if publication_type == 'manga':
                return Manga.objects.filter(work_id=work_id)
            elif publication_type == 'anime':
                return Anime.objects.filter(work_id=work_id)
            elif publication_type == 'novel':
                return Novel.objects.filter(work_id=work_id)
            else:
                return None
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publication_units_by_publication(publication):
        """Повертає публікаційні одиниці, пов'язані з публікацією"""
        try:
            return publication.publication_unit.all()
        except Exception as e:
            return None