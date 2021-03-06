from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import CategoriesMptt, ProductsMptt

from .models import Categories, Post, Good, GoodsCategories


class CountryAdmin(DjangoMpttAdmin):
    pass


admin.site.register(CategoriesMptt, CountryAdmin)


# @admin.register(Categories)
# class CatAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#     ]


# @admin.register(GoodsCategories)
# class GoodsCatAdmin(admin.ModelAdmin):
#     list_display = [
#         "name",
#     ]


# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     list_display = [
#         "id",
#         "title",
#     ]


@admin.register(ProductsMptt)
class GoodAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
