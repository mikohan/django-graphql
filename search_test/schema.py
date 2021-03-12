from graphene import String, ObjectType, Int, Field, Schema
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

# connections.create_connection(hosts=["localhost:9200"], timeout=20)
es = Elasticsearch(["http://localhost:9200"])


class Product(ObjectType):
    id = Int()
    name = String()


class Query(ObjectType):

    product = Field(Product, id=Int())

    def resolve_product(root, info, id):

        request = Search(using=es, index="prod_notebook")
        response = request.source(["id", "name"])
        for item in response:
            print(item)
        return {"id": id, "name": "Vladimir"}

    elastic = String()

    def resolve_elastic(root, info):
        return f"this is elastic"


schema = Schema(query=Query)
