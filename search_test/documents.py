from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from .models import (
    Categories,
    CategoriesMptt,
    GoodsCategories,
    Post,
    Good,
    ProductsMptt,
    Sortpos,
)
from django_elasticsearch_dsl import Document, Index, fields


@registry.register_document
class ProductsDocument(Document):

    parent = fields.ObjectField(
        properties={
            "name": fields.TextField(),
            "id": fields.IntegerField(),
        }
    )

    class Index:
        name = "products"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = ProductsMptt
        fields = ["name", "id", "slug"]
        related_models = [CategoriesMptt]

    def get_queryset(self):
        return super().get_queryset().select_related("parent")

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, CategoriesMptt):
            return related_instance.productmptt_set.all()


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
    ttext = fields.TextField(
        analyzer="rebuilt_russian", fields={"keyword": fields.Keyword()}
    )
    tname = fields.TextField(
        analyzer="rebuilt_russian", fields={"keyword": fields.Keyword()}
    )

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
                    "ngram_filter": {
                        "type": "edge_ngram",
                        "min_ngram": 2,
                        "max_ngram": 5,
                    },
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


# Add some plan
# 1. Learn all elastic search
# 2. Try to implement dsl
# 3. Try to bound graphql to elasticsearch
# 4. Configure API right way
