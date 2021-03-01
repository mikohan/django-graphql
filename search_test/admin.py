from django.contrib import admin

from .models import Categories, Post, Good, GoodsCategories


@admin.register(Categories)
class CatAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(GoodsCategories)
class GoodsCatAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
    ]
