from django.contrib import admin
from .models import Category, Tag, Post, Rating, Comment, Like


admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Like)
# admin.site.register(Post)

class RatingInline(admin.TabularInline):
    model = Rating


# fuser -k 8000/tcp
# 8001


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'category', 'get_rating')
    inlines = [RatingInline]
    search_fields = ['title', 'body']
    ordering = ['created_at']
    list_filter = ['category__title']


    def get_rating(self, obj):
        from django.db.models import Avg
        result = obj.ratings.aggregate(Avg('rating'))
        return result['rating__avg']



admin.site.register(Post, PostAdmin)
