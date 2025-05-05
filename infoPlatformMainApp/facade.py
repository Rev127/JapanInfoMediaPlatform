from .models import ServerNews, WorkNews

class NewsViewer:
    @staticmethod
    def get_server_news(news_type=None):
        """Повертає список серверних новин. За потреби — фільтрація за типом."""
        if news_type:
            return ServerNews.objects.filter(news_type=news_type).order_by('-created_at')
        return ServerNews.objects.all().order_by('-created_at')

    @staticmethod
    def get_work_news():
        """Повертає список новин, що стосуються творів."""
        return WorkNews.objects.all().order_by('-created_at')
