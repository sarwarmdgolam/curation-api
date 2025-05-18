from django.contrib import admin

from app.contents.models import Content, Category

# Register your models here.
admin.site.register(Category)
admin.site.register(Content)
