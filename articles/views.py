from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Articles
from .forms import ArticleForm
from django.http import Http404
from django.db.models import Q


def article_search_view(requests):

    query = requests.GET.get("query")
    qs = Articles.objects.search(query=query)
    context = {
        "object_list": qs
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
        return redirect(obj.get_real_url())
        # title = form.cleaned_data.get("title")
        # content = form.cleaned_data.get("content") 
        # obj = Articles.objects.create(title=title, content=content)
        # context['object'] = obj
        # context['created'] = True
    return render(requests, "articles/create.html", context=context)

def article_view(requests, slug=None):
    obj = None
    if slug is not None:
        try:
            obj = Articles.objects.get(slug=slug)
        except Articles.DoesNotExist:
            raise Http404
        except Articles.MultipleObjectsReturned:
            obj = Articles.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        'object': obj
    }
    return render(requests, "articles/details.html", context=context)
