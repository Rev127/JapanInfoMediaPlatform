from django.shortcuts import render
from .facade import NewsViewer
from apps.mediaProducts.facade import MediaProductsViewer
from apps.user.facade import UserViewer
from django.http import JsonResponse


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

def ajax_search(request):
    """Ajax пошук"""
    query = request.GET.get('q', '').strip()
    works = []
    if query:
        works = [{'title': work.get_title(), 'link': work.get_link()} for work in MediaProductsViewer.get_works_by_title_fragment(query)[:5]]
    return JsonResponse({'results': works})
