from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django_bleach.models import BleachField
from taggit.managers import TaggableManager

from datetime import datetime


class Post(models.Model):
    """Post Model"""
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(db_index=True, blank=True)
    author = models.ForeignKey(User)
    draft = models.BooleanField(db_index=True, default=True)
    tags = TaggableManager()
    body = BleachField()
    created = models.DateTimeField(auto_now_add=True)
    published = models.DateTimeField(blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published', ]

    def __unicode__(self):
        if self.draft:
            return u'[Draft:  %s by %s]' % (self.title, self.author)
        else:
            return '[%s by %s on %s]' % (self.title, self.author, self.published)

    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', [], {'slug': self.slug})

    def save(self, **kwargs):
        if self.slug == '':
            self.slug = generate_slug(Post, self.title, self.pk)
        if self.published is None or self.draft:
            self.published = datetime.now()
        super(Post, self).save()


def generate_slug(model, name, pk=None):
    count = 1
    slug = slugify(name)

    def _get_qs(model, name, pk):
        if pk is not None:
            return model.objects.filter(~Q(pk=pk), slug=slug).count()
        return model.objects.filter(slug=slug).count()

    while _get_qs(model, name, pk):
        slug = slugify(u'%s-%s' % (name, count))
        while len(slug) > model._meta.get_field('slug').max_length:
            name = name[:-1]
            slug = slugify(u'%s-%s' % (name, count))
        count = count + 1
    return slug
