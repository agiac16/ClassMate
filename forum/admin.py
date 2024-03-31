from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import ForumPost, ForumThread

# Register your models here.
admin.site.register(ForumPost)
admin.site.register(ForumThread)