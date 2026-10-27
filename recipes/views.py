from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm
from django.http import HttpResponse
from django.urls import reverse

@login_required
def recipe_list_view(requests):
    qs = Recipe.objects.filter(user=requests.user)
    context = {
        "object_list": qs
    }
    return render(requests, "recipes/list.html", context)


@login_required
def recipe_detail_view(requests, id = None):
    hx_url = reverse('recipes:hx-detail', kwargs={"id":id})
    context = {
        "hx_url": hx_url
    }
    return render(requests, "recipes/detail.html", context)


@login_required
def recipe_detail_hx_view(requests, id = None):
    try:
        obj = Recipe.objects.get(id=id, user=requests.user)
    except:
        obj = None    

    if obj is None:
        return HttpResponse("Not Found.")
    context = {
        "object": obj
    }
    return render(requests, "recipes/partials/detail.html", context)


@login_required
def recipe_create_view(requests):
    form = RecipeForm(requests.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = requests.user
        obj.save()
        return redirect(obj.get_detail_url())
    return render(requests, "recipes/create-update.html", context)


@login_required
def recipe_update_view(requests, id=None):
    obj = get_object_or_404(Recipe, id=id, user=requests.user)
    form = RecipeForm(requests.POST or None, instance=obj)
    RecipeIngredientFormset = modelformset_factory(RecipeIngredient, form=RecipeIngredientForm, extra=0)
    qs = obj.get_ingredient_list()
    formset = RecipeIngredientFormset(requests.POST or None, queryset=qs)
    context = {
        "object": obj,
        "form": form,
        "formset": formset
    }
    if form.is_valid() and formset.is_valid():
        parent = form.save(commit=False)
        parent.save()
        for ingredient_form in formset:
            child = ingredient_form.save(commit=False)
            child.recipe = parent
            child.save()
        context["message"] = "you have updated data"
    if requests.htmx:
        return render(requests, "recipes/partials/forms.html", context)
    return render(requests, "recipes/create-update.html", context)
