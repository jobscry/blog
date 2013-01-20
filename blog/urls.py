from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from posts.views import PostArchiveIndexView, PostArchiveMonthView, PostArchiveYearIndex, PostDetailView, PostListView, PostTagListView, sitemaps
from posts.feeds import PostFeed

urlpatterns = patterns('',
    url(r'^$', PostListView.as_view(), name='post_list'),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^atom\.xml$', PostFeed(), name='feed'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^archive/$', PostArchiveIndexView.as_view(), name='archive_index'),
    url(r'^archive/(?P<year>[0-9]{4})/$', PostArchiveYearIndex.as_view(), name='archive_year'),
    url(r'^archive/(?P<year>[0-9]{4})/(?P<month>[0-9]{,2})/$', PostArchiveMonthView.as_view(), name='archive_month'),
    url(r'^tags/$', PostTagListView.as_view(), {'tag': None}, name='tag_list'),
    url(r'^tag/(?P<tag>[a-zA-Z\-0-9]+)$', PostTagListView.as_view(), name='tag_detail'),
    url(r'^(?P<slug>[a-zA-Z\-0-9]+)/$', PostDetailView.as_view(), name='post_detail'),
)

handler500 = TemplateView.as_view(template_name="500.html")
handler403 = TemplateView.as_view(template_name="403.html")

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
