# THE CODE IS CLEAN

from django.contrib import admin

# Models
from .models import Person,\
                    Post,\
                    PostComment,\
                    Ad,\
                    Programming,\
                    Notification,\
                    Cloud,\
                    File


# Add models to admin panel
@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['username', 'public_email']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author']


@admin.register(PostComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'place']


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['post', 'type', 'available_views']


@admin.register(Programming)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass


class FileInline(admin.TabularInline):
    model = File


@admin.register(Cloud)
class CloudAdmin(admin.ModelAdmin):
    inlines = [FileInline]
