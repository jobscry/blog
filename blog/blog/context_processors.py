from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site


def site(request):
    return {
        'site': Site.objects.get_current(),
        'path': request.get_full_path(),
        'description': getattr(settings, 'DESCRIPTION', 'This is a blog.'),
        'copyright': getattr(settings, 'COPYRIGHT', '')
    }


def options(request):
    return {
        'snippet_length': getattr(settings, 'SNIPPET_LENGTH', 140),
    }


def flatpages(request):
    return {
        'flatpages': FlatPage.objects.filter(sites__id=settings.SITE_ID, url__iregex=r'^\/[a-z0-9\-]+\/$')
    }
