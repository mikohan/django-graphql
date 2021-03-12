from graphene import String, ObjectType, Int, Field, Schema
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField


class Product(ObjectType):
    id = Int()
    name = String()


class Query(ObjectType):

    product = Field(Product, id=Int())

    def resolve_product(root, info, id):
        return {"id": id, "name": "Vladimir"}

    elastic = String()

    def resolve_elastic(root, info):
        return f"this is elastic"


schema = Schema(query=Query)
