from django.contrib import admin

from .models import Article

# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'slug', 'modified', 'published', 'is_published')
    list_editable = ('slug', 'published', )
    search_fields = ('slug', 'summary',)
    date_hierarchy = 'modified'
    ordering = ['-modified',]
    readonly_fields = ['created', 'modified', ]

admin.site.register(Article, ArticleAdmin)
