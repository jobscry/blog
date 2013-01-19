from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    list_display = ('title', 'draft', 'published', 'created', 'modified')

admin.site.register(Post, PostAdmin)
