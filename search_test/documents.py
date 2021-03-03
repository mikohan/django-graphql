from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from .models import Categories, GoodsCategories, Post, Good, Sortpos


@registry.register_document
class PostDocument(Document):

    category = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "id": fields.IntegerField(),
        }
    )

    class Index:
        name = "posts_django"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Post
        fields = ["title", "id", "slug", "image", "description"]
        related_models = [Categories]

    def get_queryset(self):
        return super().get_queryset().select_related("category")

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, Categories):
            return related_instance.post_set.all()


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


my_analyzer = analyzer(
    "rebuilt_russian",
    tokenizer="standard",
    filter=["lowercase", "russian_stop", "russian_keywords", "russian_stemmer"],
)


@registry.register_document
class SortposDocument(Document):
    # description = fields.TextField(
    #     analyzer=my_analyzer, fields={"raw": fields.KeywordField()}
    # )
    tname = fields.Text(analyzer="standard", fields={"raw": fields.Keyword()})

    class Index:
        name = "twitter_posts"

        settings = {
            "analysis": {
                "filter": {
                    "russian_stop": {"type": "stop", "stopwords": "_russian_"},
                    "russian_keywords": {
                        "type": "keyword_marker",
                        "keywords": ["пример"],
                    },
                    "russian_stemmer": {"type": "stemmer", "language": "russian"},
                },
                "analyzer": {
                    "rebuilt_russian": {
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "russian_stop",
                            "russian_keywords",
                            "russian_stemmer",
                        ],
                    }
                },
            }
        }

    class Django:
        model = Sortpos
        fields = ["ttext"]


# Add some plan
# 1. Learn all elastic search
# 2. Try to implement dsl
# 3. Try to bound graphql to elasticsearch
# 4. Configure API right way
# 4. Configure API right way
# 4. Configure API right way
# 4. Configure API right way
# 4. Configure API right way
