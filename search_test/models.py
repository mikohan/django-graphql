from django.db import models
from django.template.defaultfilters import slugify


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


# Create your models here.
