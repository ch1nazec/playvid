from django.contrib import admin
from django.utils.html import format_html
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Tag, Videos, Comment, Channel


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name_tag',)
    search_fields = ('name_tag',)
    ordering = ('name_tag',)


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel_display', 'preview_thumbnail', 'created_date', 'like_score', 'dislike_score', 'repost_score', 'tags_list')
    list_filter = ('channel_id__channel_name', 'tag_list')
    search_fields = ('name', 'description', 'channel_id__channel_name')
    readonly_fields = ('preview_thumbnail_full',)
    filter_horizontal = ('tag_list',)
    autocomplete_fields = ('channel_id',)

    def channel_display(self, obj):
        return obj.channel_id.channel_name if obj.channel_id else '-'
    channel_display.short_description = 'Канал'

    def created_date(self, obj):
        return obj.video.name.split('/')[:4]
    created_date.short_description = 'Дата загрузки'

    def preview_thumbnail(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="height: 80px; object-fit: cover; border-radius: 4px;">', obj.preview.url)
        return "-"
    preview_thumbnail.short_description = 'Превью'

    def preview_thumbnail_full(self, obj):
        if obj.preview:
            return format_html('<img src="{}" style="max-width: 600px; height: auto;">', obj.preview.url)
        return "Нет превью"
    preview_thumbnail_full.short_description = 'Полное превью'

    def tags_list(self, obj):
        return ", ".join([tag.name_tag for tag in obj.tag_list.all()[:5]]) + ("..." if obj.tag_list.count() > 5 else "")
    tags_list.short_description = 'Теги'


@admin.register(Comment)
class CommentAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'video_link', 'channel_name', 'created_at', 'reply_count', 'is_hidden')
    list_display_links = ('indented_title',)
    list_filter = ('is_hidden', 'video__channel_id__channel_name', 'created_at')
    search_fields = ('text', 'channel__channel_name', 'video__name')
    readonly_fields = ('created_at',)
    list_per_page = 50

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('video__channel_id', 'channel')

    def video_link(self, obj):
        if obj.video:
            url = admin.site._registry[Videos].get_admin_url('change', (obj.video.pk,))
            return format_html('<a href="{}">{}</a>', url, obj.video.name[:50])
        return "-"
    video_link.short_description = 'Видео'

    def channel_name(self, obj):
        if hasattr(obj, 'channel') and obj.channel:
            return obj.channel.channel_name
        return "Неизвестно"
    channel_name.short_description = 'Автор'

    def indented_title(self, instance):
        return instance.text[:60] + ("..." if len(instance.text) > 60 else "")
    indented_title.short_description = 'Текст комментария'