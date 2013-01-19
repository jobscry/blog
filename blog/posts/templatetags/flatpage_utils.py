from django import template
from django.template.defaultfilters import stringfilter
from django.contrib.flatpages.models import FlatPage
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
@stringfilter
def fpcrumbs(url, title, autoescape=None):
    pages = url.split('/')
    for index, item in enumerate(pages):
        if item == '':
            del pages[index]
    num = len(pages)
    if num <= 1:
        return ''
    else:
        string = u'<ul class="breadcrumb">'
        for page in pages:
            fp = FlatPage.objects.filter(url='/' + page + '/')
            if fp:
                string = u'%s<li><a href="%s" title="%s">%s</a> <span class="divider">/</span></li>' % (string, fp[0].url, fp[0].title, fp[0].title)
    return mark_safe(u'%s<li class="active">%s</li></ul>' % (string, title))
