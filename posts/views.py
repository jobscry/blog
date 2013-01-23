from django.conf import settings
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.views.generic import ArchiveIndexView, DetailView, ListView, MonthArchiveView, YearArchiveView
from taggit.models import TaggedItem
from posts.models import Post

PAGINATE_BY = getattr(settings, 'PAGINATE_BY', 20)

info_dict = {
    'queryset': Post.objects.filter(draft=False),
    'date_field': 'published',
}

sitemaps = {
    'flatpages': FlatPageSitemap,
    'blog': GenericSitemap(info_dict, priority=0.6),
}


class PostView(object):
    def get_queryset(self):
        if(self.request.user.is_authenticated()):
            return Post.objects.filter(author=self.request.user)
        else:
            return Post.objects.filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['active_page'] = 'post_list'
        return context


class PostDateView(PostView):
    date_field = 'published'


class PostArchiveIndexView(PostDateView, ArchiveIndexView):
    pass


class PostArchiveMonthView(PostDateView, MonthArchiveView):
    month_format = '%m'


class PostArchiveYearIndex(PostDateView, YearArchiveView):
    pass


class PostDetailView(PostView, DetailView):
    pass


class PostListView(PostView, ListView):
    paginate_by = PAGINATE_BY


class PostTagListView(ListView):
    template_name = 'posts/tag_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostTagListView, self).get_context_data(**kwargs)
        context['active_page'] = 'post_list'
        if self.kwargs['tag'] is not None:
            context['post_list'] = Post.objects.filter(draft=False, tags__name__in=[self.kwargs['tag'], ]).distinct()
            context['tag'] = self.kwargs['tag']
        return context

    def get_queryset(self):
        return TaggedItem.tags_for(Post)
