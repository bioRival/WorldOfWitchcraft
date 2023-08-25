from django.contrib import admin
from .models import Post, Author, PostReply

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(PostReply)
