from django.contrib import admin
from .models import Post, BlogComment
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    fields=['title','author','content','likes'] 
    list_display=('title','author','content')
    search_fields=['title','author']
admin.site.register(Post,PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('author','content')
    search_fields=['author']
admin.site.register(BlogComment,CommentAdmin)