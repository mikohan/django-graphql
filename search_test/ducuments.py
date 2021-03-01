from django_elasticsearch_dsl import DocType, Index
from .models import Post

posts = Index("dnago_posts")


@posts.doc_type
class PostDocument(DocType):
    class Meta:
        model = Post

        fields = ["title", "id", "slug", "image" "description"]
