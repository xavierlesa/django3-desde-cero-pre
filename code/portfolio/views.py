from django.shortcuts import render, get_object_or_404
from .models import Project


def project_list(request):
    qs = Project.objects.all()
    return render(request, 'portfolio/list.html', {
        'objects': qs
    })


def project_detail(request, slug=None):
    qs = get_object_or_404(Project, slug=slug)
    return render(request, 'portfolio/detail.html', {
        'object': qs
    })


def project_filter_list(request, tag=None):
    qs = Project.objects.filter(tags__slug__in=[tag])
    return render(request, 'portfolio/list.html', {
        'objects': qs
    })
