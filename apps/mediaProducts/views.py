from django.contrib.admin import action
from django.shortcuts import render, redirect

from .facade import MediaProductsViewer
from apps.user.facade import UserViewer
from django.contrib import messages

# Create your views here.
def work_view(request, link):
    work = MediaProductsViewer.get_work_info(link)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'track':
            if MediaProductsViewer.track_work(request.user, work):
                messages.success(request, "Work tracked successfully.")
            else:
                messages.error(request, "Work tracking failed.")
        elif action == 'untrack':
            if MediaProductsViewer.untrack_work(request.user, work):
                messages.success(request, "Work untracked successfully.")
            else:
                messages.error(request, "Work untracking failed.")
        return redirect('work', link=link)

    publications = MediaProductsViewer.get_publications_by_work(link)
    is_tracked = False
    if request.user.is_authenticated:
        is_tracked = request.user.work_is_tracked(work)
    return render(request, 'mediaProducts/work.html', {
        'work': work,
        'publications': publications,
        'is_tracked': is_tracked
    })

def publication_view(request, publication_type, link):
    publication = MediaProductsViewer.get_publication_by_type(publication_type, link)
    if publication:
        publication_unit = MediaProductsViewer.get_publication_units_by_publication(publication)
    else:
        publication_unit = None
    return render(request, 'mediaProducts/publication.html', {
        'type': publication_type,
        'publication': publication,
        'publication_unit': publication_unit
    })

def publication_unit_view(request, publication_unit_type, link):
    publication_unit = MediaProductsViewer.get_publication_unit_by_type_and_link(publication_unit_type, link)
    if publication_unit:
        comments = UserViewer.get_comments_by_publication_unit(publication_unit.id)
    else:
        comments = None

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add_comment':
            content = request.POST.get('comment')
            if content:
                comment = UserViewer.add_comment(request.user, publication_unit, content)
                if comment:
                    messages.success(request, "Коментар успішно додано.")
                else:
                    messages.error(request, "Додати коментар не вдалося.")
            else:
                messages.error(request, "Коментар не може бути порожнім.")
            return redirect('publication_unit', publication_unit_type=publication_unit_type, link=link)

    return render(request, 'mediaProducts/publication_unit.html', {
        'type': publication_unit_type,
        'publication_unit': publication_unit,
        'comments': comments
    })
