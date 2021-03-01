from django.db import models


class Categories(models.Model):

    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        "self", on_delete=models.DO_NOTHING, related_name="parent_reverce"
    )

    def __str__(self):
        return self.name


class Post(models.Model):

    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="posts")


# Create your models here.
