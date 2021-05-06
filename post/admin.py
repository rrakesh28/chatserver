
from django.contrib import admin

from post.models import Post

class PostAdmin(admin.ModelAdmin):
    list_filter = ['creator']
    list_display = ['creator']
    search_fields = ['creator__username']
    readonly_fields = ['id']

    class Meta:
        model = Post


admin.site.register(Post, PostAdmin)



