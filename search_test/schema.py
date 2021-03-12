from graphene import String, ObjectType, Int, ID, Field, Schema, Interface, List
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
import requests, json


# connections.create_connection(hosts=["localhost:9200"], timeout=20)
es = Elasticsearch(["http://localhost:9200"])


class ICategories(Interface):
    cat_id = ID(required=True)
    cat_name = String(required=True)
    cat_parent = ID(required=False)


class IEngines(Interface):
    engine_id = ID()
    engine_name = String()


class ICarModels(Interface):
    model_id = ID()
    model_name = String()


class IBrand(Interface):
    brand_id = ID()
    brand_name = String()
    brand_slug = String()


class CarModel(ObjectType):
    class Meta:
        interfaces = (ICarModels,)


class Cats(ObjectType):
    class Meta:
        interfaces = (ICategories,)


class Engines(ObjectType):
    class Meta:
        interfaces = (IEngines,)


class Brand(ObjectType):
    class Meta:
        interfaces = (IBrand,)


class ProductSource(ObjectType):

    name = String()
    categories = List(Cats)
    brand = Field(Brand)
    car_model = List(CarModel)
    engines = List(Engines)


class Product(ObjectType):
    _index = String(required=False)
    _id = Int()
    _source = Field(ProductSource)


class Query(ObjectType):

    product = List(Product, query=String())

    def resolve_product(root, info, query):
        data = json.dumps(
            {"size": 1000, "query": {"term": {"car_model.model_name.keyword": query}}}
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
        print(result[0]["_source"]["engines"])

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
