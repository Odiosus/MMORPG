from django.contrib import admin
from .models import Category, Post, Comment, NewsForSubscribers, SubscriberNews


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'heading', 'content', 'category', 'pub_date')
    list_display_links = ('heading', 'content')
    list_filter = ('category', 'pub_date', )
    search_fields = ['author', 'heading', 'content']
    ordering = ['-pub_date']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post_comment', 'confirm', 'date_comment')
    list_display_links = ('author', 'text', 'confirm')
    list_filter = ('author', 'text', 'post_comment', 'confirm', 'date_comment')
    search_fields = ('author', 'post_comment', 'confirm', 'date_comment')
    ordering = ['-date_comment']


@admin.register(NewsForSubscribers)
class NewsForSubscribersAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'draft', 'pub_date')
    list_display_links = ('title', 'content')
    list_filter = ('draft', 'pub_date', )
    search_fields = ['title', 'content']
    ordering = ['-pub_date']


@admin.register(SubscriberNews)
class SubscriberNewsAdmin(admin.ModelAdmin):
    list_display = ('user', )
    list_display_links = ('user', )
    search_fields = ['user']