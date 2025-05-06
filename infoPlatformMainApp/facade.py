from .models import ServerNews, WorkNews

class NewsViewer:
    @staticmethod
    def get_server_news():
        """Повертає список серверних новин."""
        return ServerNews.objects.all().order_by('-created_at')

    @staticmethod
    def get_work_news():
        """Повертає список новин, що стосуються творів."""
        return WorkNews.objects.all().order_by('-created_at')
