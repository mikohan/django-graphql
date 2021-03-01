from django.db import models


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

    def __str__(self):
        return self.name


class Post(models.Model):

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="posts")
    slug = models.SlugField(blank=True)

    def __str__(self):
        return f"{self.title}-{self.category.name}"


# Create your models here.
