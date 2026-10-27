from django.db import models
from django.conf import settings
from .validators import valid_units_check
from .utils import number_str_to_float
from django.urls import reverse
import pint
from django.db.models import Q



class RecipesQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = Q(name__icontains=query) | Q(description__icontains=query) | Q(directions__icontains=query)
        return self.filter(lookups)

class RecipesManager(models.Manager):
    def get_queryset(self):
        return RecipesQuerySet(self.model, using=self._db)
    
    def search(self, query=None):  
        return self.get_queryset().search(query=query)


class Recipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = RecipesManager()

    @property
    def title(self):
        return self.name

    def get_detail_url(self):
        return reverse('recipes:detail', kwargs={"id":self.id})

    def get_delete_url(self):
        return reverse('recipes:delete', kwargs={"id":self.id})

    def get_real_url(self):
            return reverse('recipes:detail', kwargs={"id":self.id})

    def get_hx_url(self):
        return reverse('recipes:hx-detail', kwargs={"id":self.id})

    def get_edit_url(self):
        return reverse('recipes:update', kwargs={"id":self.id})

    def get_ingredient_list(self):
        return self.recipeingredient_set.all()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    directions = models.TextField(blank=True, null=True)
    quantity  = models.CharField(max_length=40)
    quantity_as_float = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=20, validators=[valid_units_check])
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


    def get_real_url(self):
        return self.recipe.get_detail_url()

    def get_delete_url(self):
        kwargs={
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:ingredient-delete", kwargs=kwargs)

    def get_hx_edit_url(self):
        kwargs={
            "parent_id": self.recipe.id,
            "id": self.id
        }
        return reverse("recipes:hx-ingredient-update", kwargs=kwargs)

    def change_system_units(self, system="mks"):
        if self.quantity_as_float is None:
            return None
        ureg = pint.UnitRegistry(system=system)
        measurement = self.quantity_as_float * ureg(self.unit)
        return measurement

    def as_mks(self):
        measurement = self.change_system_units(system="mks")
        return measurement.to_base_units()

    def as_imperial(self):
            measurement = self.change_system_units(system="imperial")
            return measurement.to_base_units()

    def save(self, *args, **kwargs):
        qt = self.quantity
        qty_as_float, success = number_str_to_float(qt)
        if success:
            self.quantity_as_float = qty_as_float
        else:
            self.quantity_as_float = None

        super().save(*args, **kwargs)
    
