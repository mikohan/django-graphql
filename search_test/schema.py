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


## Start aggregations
class IBucket(Interface):
    key = String()
    doc_count = Int()


class Bucket(ObjectType):
    class Meta:
        interfaces = (IBucket,)


class CarModelsAgg(ObjectType):
    buckets = List(Bucket)


class CategoriesAgg(ObjectType):
    buckets = List(Bucket)


class Aggregations(ObjectType):
    car_models = List(CarModelsAgg)
    categories = List(CategoriesAgg)


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


class Root(ObjectType):
    product = List(Product)
    aggregations = Field(Aggregations)


class Query(ObjectType):

    root = Field(Root, query=String())

    def resolve_root(root, info, query):
        # data = json.dumps(
        #     {"size": 1000, "query": {"term": {"car_model.model_name.keyword": query}}}
        # )
        data_aggs = json.dumps(
            {
                "size": 1,
                "query": {"match": {"categories.cat_parent": query}},
                "aggs": {
                    "categories": {"terms": {"field": "categories.cat_name.keyword"}},
                    "brands": {"terms": {"field": "brand.brand_name.keyword"}},
                    "engines": {"terms": {"field": "engines.engine_name.keyword"}},
                    "car_models": {"terms": {"field": "car_model.model_name.keyword"}},
                },
            }
        )

        r = requests.get(
            "http://localhost:9200/prod_notebook/_search",
            headers={"Content-Type": "application/json"},
            data=data_aggs,
        )
        response = r.json()

        result = response  # ["hits"]
        aggs = response["aggregations"]
        print(aggs)

        return {"product": result, "aggregations": aggs}

    elastic = String()

    def resolve_elastic(root, info):
        return f"this is elastic"


schema = Schema(query=Query)
