from django.views.generic.base import TemplateView
from django.http import JsonResponse
from .models import Post
import json, requests


class SearchView(TemplateView):
    template_name = "search.html"

    # def get_context_data(self, *args, **kwargs):
    #     q = self.request.GET.get("q")
    #     if q:
    #         posts = PostDocument.search().query("match", title=q)
    #     else:
    #         posts = [{"title": "Not founda", "image": None}]
    #     context = super().get_context_data(**kwargs)
    #     context["objects"] = posts
    #     context["objects_qs"] = posts.to_queryset()
    #     return context


# Create your views here.
# Plan for long
# 1. Add fields to model
# 2. Copy real data from Remote table to local for testes
# 3. Design and create calss for inserting data into Elasticsearch
# 4. Design and create Price model
# 5. Design and create Stock model
# 6. Start working with Front End

# For Tomorrow
# 1. Design and Create price model
# 2. Desing and create Stock model
# 4. Add all fields to model
# 5. Start testing frontend


def send_json(request):
    query = request.GET.get("q")
    if not query:
        query = 1
    data_aggs = json.dumps(
        {
            "size": 20,
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
    data = response

    return JsonResponse(data, safe=False)
