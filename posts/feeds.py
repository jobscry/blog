from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.core.urlresolvers import reverse
from posts.models import Post

site = Site.objects.get_current()
description = getattr(settings, 'DESCRIPTION', 'This is a blog.')
author = getattr(settings, 'AUTHOR', 'An Author')
copyright = getattr(settings, 'COPYRIGHT', 'Copyright (c) 2013 ' + author)
num_entries = getattr(settings, 'PAGINATE_BY', 20)

class PostFeed(Feed):
    def title(self):
        return site.name

    def link(self):
        return site.domain + '/'

    def feed_link(self):
        return reverse('feed')

    def description(self):
        return description

    def author_name(self):
        return author

    def feed_copyright(self):
        return copyright

    def items(self):
        return Post.objects.filter(draft=False)[:num_entries]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_author_name(self, item):
        return item.author.get_full_name()

    def item_pubdate(self, item):
        return item.published

    def item_categories(self, item):
        return item.tags.all()

