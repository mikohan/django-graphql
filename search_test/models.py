from django.db import models
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey


class Categories(models.Model):

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self",
        on_delete=models.DO_NOTHING,
        related_name="parent_reverce",
        null=True,
        blank=True,
    )
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class GoodsCategories(models.Model):

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Good(models.Model):

    category = models.ForeignKey(GoodsCategories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="posts")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}-{self.category.name}"


class Post(models.Model):

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="posts")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}-{self.category.name}"


class Sortpos(models.Model):

    tname = models.CharField(max_length=255)
    ttext = models.TextField()

    def __str__(self):
        return self.tname


# Create your models here.


class CategoriesMptt(MPTTModel):

    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductsMptt(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    parent = models.ForeignKey(CategoriesMptt, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
