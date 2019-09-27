from django.contrib import admin

from .models import Comment

from typeidea.custom_site import custom_site

@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target', 'nickname', 'content', 'website', 'created_time')

#由于comment的model中没有user这个性质，所以不必要支出user来储存，所以不必更改save_model函数