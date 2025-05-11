from django.shortcuts import render
from django.template.defaulttags import comment

from .facade import MediaProductsViewer
from apps.user.facade import UserViewer

# Create your views here.
def work_view(request, link):
    work = MediaProductsViewer.get_work_info(link)
    publications = MediaProductsViewer.get_publications_by_work(link)
    return render(request, 'mediaProducts/work.html', {
        'work': work,
        'publications': publications
    })

def publication_view(request, type, link):
    publication = MediaProductsViewer.get_publication_by_type(type, link)
    if publication:
        publication_unit = MediaProductsViewer.get_publication_units_by_publication(publication)
    else:
        publication_unit = None
    return render(request, 'mediaProducts/publication.html', {
        'type': type,
        'publication': publication,
        'publication_unit': publication_unit
    })

def publication_unit_view(request, type, link):
    publication_unit = MediaProductsViewer.get_publication_unit_by_type_and_link(type, link)
    if publication_unit:
        comments = UserViewer.get_comments_by_publication_unit(publication_unit.id)
    else:
        comments = None

    return render(request, 'mediaProducts/publication_unit.html', {
        'type': type,
        'publication_unit': publication_unit,
        'comments': comments
    })
