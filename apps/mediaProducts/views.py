from django.shortcuts import render


def work_view(request):
    return render(request, 'mediaProducts/work.html')

def publication_view(request):
    return render(request, 'mediaProducts/publication.html')

def publication_unit_view(request):
    return render(request, 'mediaProducts/publication_unit.html')