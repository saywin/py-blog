from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from blog.models import User, Commentary, Post

admin.site.unregister(Group)


@admin.register(User)
class MyUserAdmin(UserAdmin):
    pass


@admin.register(Commentary)
class CommentaryAdmin(admin.ModelAdmin):
    list_display = ["id", "created_time", "user_name", "post_title"]
    search_fields = ["created_time", "user__username", "post__title"]
    list_filter = ["created_time"]

    def user_name(self, obj):
        return obj.user.username

    user_name.short_description = "Writer"

    def post_title(self, obj):
        return obj.post.title

    post_title.short_description = "Post"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_time", "user_name"]
    search_fields = ["title", "created_time", "owner__username"]
    list_filter = ["created_time"]

    def user_name(self, obj):
        return obj.owner.username

    user_name.short_description = "Writer"
