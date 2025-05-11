from django.shortcuts import render
from .facade import NewsViewer
from apps.mediaProducts.facade import MediaProductsViewer
from apps.user.facade import UserViewer


# Create your views here.

def index(request):
    """Головна сторінка"""
    server_news = NewsViewer.get_server_news()
    work_news = NewsViewer.get_work_news()
    last_update_works = MediaProductsViewer.get_last_update_work()
    user_id = request.user.id
    user = UserViewer.get_user_by_id(user_id)

    return render(request, 'mainapp/index.html', {
        'server_news': server_news,
        'work_news': work_news,
        'last_update_works': last_update_works,
        'user': user
    })
