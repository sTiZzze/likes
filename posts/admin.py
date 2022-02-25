from posts.models import Post
from django.contrib import admin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')


admin.site.register(Post, ProfileAdmin)
