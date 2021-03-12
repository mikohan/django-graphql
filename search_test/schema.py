from graphene import String, ObjectType, Int, ID, Field, Schema, Interface, List
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
import requests, json


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
es = Elasticsearch(["http://localhost:9200"])


class ICategories(Interface):
    cat_parent = ID(required=True)
    cat_name = String(required=True)
    cat_parent = ID(required=False)


class IProduct(Interface):
    id = ID(required=True)
    name = String(required=True)
    categories = List(ICategories)


class CategoriesSource(ObjectType):

    _id = ID()
    _source = Field("Categories")


class Categories(ObjectType):
    cat_name = String()
    cat_parent = ID()


class ProductSource(ObjectType):

    name = String()
    categories = Field(CategoriesSource)
    # brand = Field(Brand)
    # car_model = Field(CarModel)


class Product(ObjectType):
    _index = String(required=False)
    _id = Int()
    _source = Field(ProductSource)


class Query(ObjectType):
    class Meta:
        interfaces = (ICategories, IProduct)

    product = List(Product)

    def resolve_product(root, info):
        data = json.dumps(
            {"size": 10, "query": {"term": {"car_model.model_name.keyword": "HD72"}}}
        )
        # data_aggs = json.dumps(
        #     {
        #         "size": 1,
        #         "query": {"match": {"categories.cat_parent": id}},
        #         "aggs": {
        #             "categories": {"terms": {"field": "categories.cat_name.keyword"}},
        #             "brands": {"terms": {"field": "brand.brand_name.keyword"}},
        #             "engines": {"terms": {"field": "engines.engine_name.keyword"}},
        #             "car_models": {"terms": {"field": "car_model.model_name.keyword"}},
        #         },
        #     }
        # )

        r = requests.get(
            "http://localhost:9200/prod_notebook/_search",
            headers={"Content-Type": "application/json"},
            data=data,
        )
        response = r.json()

        result = response["hits"]["hits"]
        print(result[0])

        # request = Search(using=es, index="prod_notebook")
        # response = request.source(["id", "name"])
        # for item in response:
        #     print(item)
        # return json.loads(result)
        return result

    elastic = String()

    def resolve_elastic(root, info):
        return f"this is elastic"


schema = Schema(query=Query)
