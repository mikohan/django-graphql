from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Categories, GoodsCategories, Post, Good


@registry.register_document
class PostDocument(Document):

    category = fields.ObjectField(
        properties={"name": fields.TextField(), "id": fields.IntegerField()}
    )

    class Index:
        name = "posts_django"
        ettings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Post
        fields = ["title", "id", "slug", "image", "description"]
        related_models = [Categories]

    def get_queryset(self):
        return super().get_queryset().select_related("category")


@registry.register_document
class GoodDocument(Document):
    class Index:
        name = "good_django"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    category = fields.ObjectField(
        properties={"name": fields.TextField(), "id": fields.IntegerField()}
    )

    class Django:
        model = Good
        fields = ["title", "id", "slug", "image", "description"]
        related_models = [GoodsCategories]

    def get_queryset(self):
        return super().get_queryset().select_related("category")
