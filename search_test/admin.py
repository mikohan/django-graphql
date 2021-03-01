from django.contrib import admin

from .models import Categories, Post


@admin.register(Categories)
class CatAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Post)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
