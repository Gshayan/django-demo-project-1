from django.contrib import admin

from .models import Recipe, RecipeIngredient

class RecipeIngredientInline(admin.StackedInline):
    model = RecipeIngredient
    extra = 0
    readonly_fields = ['quantity_as_float', 'as_mks', 'as_imperial']

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ['user', 'name']
    readonly_fields = ['timestamp', 'updated',]


admin.site.register(Recipe, RecipeAdmin)

