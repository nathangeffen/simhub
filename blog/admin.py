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
    actions_on_bottom = True
    actions_on_top = True
    save_on_top = True

admin.site.register(Article, ArticleAdmin)

admin.site.site_header = "Simhub admin"
admin.site.site_title = "Simhub site admin"
admin.site.index_title = "Simhub administration"
