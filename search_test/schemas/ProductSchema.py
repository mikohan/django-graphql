from graphene import String, ObjectType, Int, ID, Field, Schema, Interface, List
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
import requests, json
from .GraphqlInterfaces import *


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


class Bucket(ObjectType):
    class Meta:
        interfaces = (IBucket,)


class CarModelsAgg(ObjectType):
    buckets = List(Bucket)


class CategoriesAgg(ObjectType):
    buckets = List(Bucket)


class Aggregations(ObjectType):
    car_models = Field(CarModelsAgg)
    categories = Field(CategoriesAgg)


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
