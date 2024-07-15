from django.contrib import admin
from .models import Post, Category, PostCategory, Comment, Subscription, Author


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'category_type', 'rating')
    list_filter = ('title', 'text', 'category_type', 'rating')
    search_fields = ('title', 'text')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Subscription)