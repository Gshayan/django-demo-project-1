from django import forms

from .models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    required_css_class = "required-fields-class"
    error_css_class = "error-field"
    name = forms.CharField(help_text="forget name")
    class Meta:
        model = Recipe
        fields = ["name", "description", "directions"]

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            dict = {
                "placeholder": f"Recipe {str(field)}",
                "class": "form-control-2",
                # "hx-post": ".",
                # "hx-trigger": "keyup changed delay:500ms",
                # "hx-target": "#recipe-container",
                # "hx-swap": "outerHTML"
            }
            self.fields[str(field)].widget.attrs.update(dict)
        self.fields["description"].widget.attrs.update({"rows": "2"})
        self.fields["directions"].widget.attrs.update({"rows": "4"})


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ["name", "quantity", "unit"]