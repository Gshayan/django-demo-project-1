from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Articles
from .forms import ArticleForm
# from django.http import HttpResponse

def article_search_view(requests):

    query_dictionary = requests.GET
 
    try:
        query = int(query_dictionary.get("query"))
    except:
        query = None

    obj = None
    if query is not None:
        obj = Articles.objects.get(id=query)
    context = {
        "object": obj
    }
    return render(requests, "articles/search.html", context=context)

# @login_required
# def article_create_view(requests):
    
#     form = ArticleForm()
#     context = {
#         "form": form
#     }
#     if requests.method=="POST":
#         form = ArticleForm(requests.POST)
#         context["form"] = form
#         if form.is_valid():
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content") 
#             obj = Articles.objects.create(title=title, content=content)
#             context['object'] = obj
#             context['created'] = True
#     return render(requests, "articles/create.html", context=context)

@login_required
def article_create_view(requests):
    
    form = ArticleForm(requests.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save()
        context["form"] = ArticleForm()
        # title = form.cleaned_data.get("title")
        # content = form.cleaned_data.get("content") 
        # obj = Articles.objects.create(title=title, content=content)
        # context['object'] = obj
        # context['created'] = True
    return render(requests, "articles/create.html", context=context)

def article_view(requests, id=None):
    obj = None
    if id is not None:
        obj = Articles.objects.get(id=id)
        
    context = {
        'object': obj
    }
    return render(requests, "articles/details.html", context=context)
