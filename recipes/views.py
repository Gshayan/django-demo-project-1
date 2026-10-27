from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from .models import Recipe, RecipeIngredient
from .forms import RecipeForm, RecipeIngredientForm
from django.http import HttpResponse, Http404
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
def recipe_delete_view(requests, id = None):
    try:
        obj = Recipe.objects.get(id=id, user=requests.user)
    except:
        obj = None
    if obj is None:
        if requests.htmx:
            return HttpResponse("Not Found.")
        raise Http404
    
    # obj = get_object_or_404(Recipe, id=id, user=requests.user)
    if requests.method == "POST":
        obj.delete()
        url = reverse("recipes:list")
        if requests.htmx:
            headers = {
                "HX-Redirect": url
            }
            return HttpResponse("Success", headers=headers)
        return redirect(url)
    context = {
        "object": obj
    }
    return render(requests, "recipes/delete.html", context)


@login_required
def recipe_ingredient_delete_view(requests, parent_id=None, id = None):
    try:
        obj = RecipeIngredient.objects.get(recipe__id=parent_id, id=id, recipe__user=requests.user)
    except:
        obj = None
    if obj is None:
        if requests.htmx:
            return HttpResponse("Not Found.")
        raise Http404
    
    if requests.method == "POST":
        name = obj.name
        obj.delete()
        url = reverse("recipes:detail", kwargs={"id":parent_id})
        if requests.htmx:
            return render(requests, "recipes/partials/ingrefdient-inline-delete-response.html", {"name":name})
        return redirect(url)
    context = {
        "object": obj
    }
    return render(requests, "recipes/delete.html", context)


@login_required
def recipe_detail_hx_view(requests, id = None):
    if not requests.htmx:
        raise Http404
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
        if requests.htmx:
            headers={
                "HX-Redirect": obj.get_detail_url()
            }
            return HttpResponse("Created", headers=headers)
            # context = {
            #     "object": obj
            # }
            # return render(requests, "recipes/partials/detail.html", context)
        return redirect(obj.get_detail_url())
    return render(requests, "recipes/create-update.html", context)


@login_required
def recipe_update_view(requests, id=None):
    obj = get_object_or_404(Recipe, id=id, user=requests.user)
    form = RecipeForm(requests.POST or None, instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id":obj.id})
    context = {
        "object": obj,
        "form": form,
        "new_ingredient_url": new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context["message"] = "Data Saved!"
    if requests.htmx:
        return render(requests, "recipes/partials/forms.html", context)
    return render(requests, "recipes/create-update.html", context)


@login_required
def recipe_ingredient_update_hx_view(requests, parent_id=None, id = None):
    if not requests.htmx:
        raise Http404
    try:
        parent_obj = Recipe.objects.get(id=parent_id, user=requests.user)
    except:
        parent_obj = None    

    if parent_obj is None:
        return HttpResponse("Not Found.")


    instance = None
    if id is not None:
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            instance = None

    form = RecipeIngredientForm(requests.POST or None, instance=instance)
    url = instance.get_hx_edit_url() if instance else reverse("recipes:hx-ingredient-create", kwargs={"parent_id":parent_obj.id})
    context = {
        "url": url,
        "object": instance,
        "form": form
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:
            new_obj.recipe = parent_obj
        new_obj.save()
        context["object"] = new_obj
        return render(requests, "recipes/partials/ingredient-inline.html", context)
    return render(requests, "recipes/partials/ingredient-form.html", context)