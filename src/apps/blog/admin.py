from django.contrib import admin

from .models import Article, ArticleRate, ArticleSubscribe, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'id', 'get_str_tag_list',
        'default_tag', 'owner', 'create_at', 'update_at'
    )
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('owner', 'title', 'slug', 'tags', 'default_tag', 'image_header', 'body')
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'admin_thumbnail', 'id', 'get_num_articles_in_tag', 'views')
    readonly_fields = ('admin_thumbnail',)


@admin.register(ArticleSubscribe)
class ArticleSubscribeAdmin(admin.ModelAdmin):
    pass


@admin.register(ArticleRate)
class ArticleRateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'positives')
