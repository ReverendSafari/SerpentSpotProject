
from django.contrib import admin
from Forum.models import Thread, Post, Board, PostImage

# Register your models here.
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(Board)
admin.site.register(PostImage)