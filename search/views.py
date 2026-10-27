from django.shortcuts import render
from articles.models import Articles
from recipes.models import Recipe

Search_Type_Mapping = {
    "article": Articles,
    "articles": Articles,
    "recipe": Recipe,
    "recipes": Recipe
}

def search_view(requests):
    query = requests.GET.get("q")
    search_type = requests.GET.get("type")
    Klass = Recipe
    if search_type in Search_Type_Mapping.keys():
        Klass = Search_Type_Mapping[search_type]
    qs = Klass.objects.search(query=query)
    context = {
        "queryset": qs
    }
    template = "search/results-view.html"
    if requests.htmx:
        context["queryset"] = qs[:3]
        template = "search/partials/results.html"
    return render(requests, template, context)