from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.admin.models import LogEntry

from .models import Post, Category, Tag
from .adminforms import PostAdminForm

from typeidea.custom_site import custom_site 
from typeidea.base_admin import BaseOwnerAdmin


class PostInline(admin.StackedInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post

@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    inlines = [PostInline, ]
    list_display = (
        'name', 'status', 'is_nav', 'created_time','owner', 
        'post_count'
    )
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'created_time','owner')
    fields = ('name', 'status')


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = '分类过滤器'
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    list_display = (
        'title', 'category', 'status','owner',
        'created_time', 'operator', 'comment_count'
    )
    list_display_links = []

    list_filter = [CategoryOwnerFilter, ]
    search_fields = ['title', 'category__name']

    actions_on_top = True
    actions_on_bottom = True

    #编辑页面
    save_on_top = True

    exclude = ['owner',]
    """
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )
    """
    fieldsets = (
        ('基础配置', {
            #'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('wide',),
            'fields': ('tag', ),
        })
    )
    filter_horizontal = ('tag', )
    #filter_vertical = ('tag', )


    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def comment_count(self, obj):
        return obj.comment_set.count()

    comment_count.short_description = "评论数量"
    

    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css", ),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js', )


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = [
        'object_repr', 'object_id', 'action_flag', 'user', 'change_message',
        'content_type', 'action_time'
    ]

# Register your models here.
