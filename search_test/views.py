from django.views.generic.base import TemplateView
from django.http import HttpResponse
from .models import Post


class SearchView(TemplateView):
    template_name = "search.html"

    def get_context_data(self, *args, **kwargs):
        print(self.request.GET.get("q"))
        context = super().get_context_data(**kwargs)
        context["objects"] = Post.objects.all()
        return context


# Create your views here.
