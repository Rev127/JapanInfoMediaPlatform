from .models import Work, Manga, Anime, Novel, Volumes, Seasons
from django.db.models import Max

class MediaProductsViewer:
    @staticmethod
    def get_work_info(link):
        """Повертає інформацію про твір за ID"""
        try:
            return Work.objects.prefetch_related('genre').select_related('author').get(link=link)
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
    def get_publications_by_work(link):
        """Повертає публікації, пов'язані з твором"""
        try:
            manga = Manga.objects.filter(work__link=link)
            anime = Anime.objects.filter(work__link=link)
            novel = Novel.objects.filter(work__link=link)
            return {
                'manga': manga,
                'anime': anime,
                'novel': novel
            }
        except Work.DoesNotExist:
            return None

    @staticmethod
    def get_publication_by_type(publication_type, link):
       """Повертає публікацію за типом"""
       try:
           if publication_type == 'manga':
               return Manga.objects.filter(link=link).first()
           elif publication_type == 'anime':
               return Anime.objects.filter(link=link).first()
           elif publication_type == 'novel':
               return Novel.objects.filter(link=link).first()
           else:
               return None
       except Exception:
           return None

    @staticmethod
    def get_publication_units_by_publication(publication):
        """Повертає публікаційні одиниці, пов'язані з публікацією"""
        try:
            return publication.publication_unit.all()
        except Exception as e:
            return None

    @staticmethod
    def get_publication_unit_by_type_and_link(publication_unit_type, publication_unit_link):
        """Повертає публікаційну одиницю за посиланням"""
        try:
            if publication_unit_type == 'volume':
                return Volumes.objects.get(link=publication_unit_link)
            elif publication_unit_type == 'season':
                return Seasons.objects.get(link=publication_unit_link)
            else:
                return None
        except Exception:
            return None

    @staticmethod
    def track_work(user, work):
        """Додає твір до відстежуваних"""
        if not user.work_is_tracked(work):
            user.tracking_works.add(work)
            return True
        return False

    @staticmethod
    def untrack_work(user, work):
        """Видаляє твір з відстежуваних"""
        if user.work_is_tracked(work):
            user.tracking_works.remove(work)
            return True
        return False

    @staticmethod
    def get_works_by_title_fragment(title):
        """Повертає твір за назвою"""
        try:
            return Work.objects.filter(title__icontains=title)
        except Work.DoesNotExist:
            return None