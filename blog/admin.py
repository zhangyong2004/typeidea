from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Category, Tag, Post
from blog.adminforms import PostAdminForm


# Register your models here.
from typeidea.custom_site import custom_site

#注册添加分类管理模块
@admin.register(Category,site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'

#注册添加标签管理模块
@admin.register(Tag,site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

#注册添加文章管理模块
@admin.register(Post,site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

    list_display = ('title', 'category', 'status', 'created_time', 'operator')
    list_display_links = ()
    list_filter = ('category',)
    search_fields = ('title', 'category_name')

    # actions_on_top = True
    # actions_on_bottom = True

    save_on_top = True

    # exclude = ('owner',)
    # fields = (('category','title'),'desc','status','content','tag')
    fieldsets = (
        ('基础配置', {'description': '基础配置描述', 'fields': (('title', 'category'), 'status')}),
        ('内容', {'fields': ('desc', 'content')}),
        ('额外信息', {'classes': ('collapse',), 'fields': ('tag',)})
    )

    # filter_vertical = ('tag',)

    def operator(self, obj):
        return format_html('<a href="{}">编辑</a>', reverse('cus_admin:blog_post_change', args=(obj.id,)))

    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    # class Media:
    #     css={'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css',),}
    #     js=('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)


#注册添加日志管理模块
@admin.register(LogEntry,site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr','object_id','action_flag','user','change_message']