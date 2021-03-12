from search_test.views import SearchView, send_json
from django.urls import path

from graphene_django.views import GraphQLView

from .schema import schema

urlpatterns = [
    # Only a single URL to access GraphQL
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),
    path("query", SearchView.as_view(), name="search"),
    path("jsontest", send_json, name="send_json"),
]
