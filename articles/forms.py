from django import forms
from .models import Articles

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content']

    def clean(self):
        data = self.cleaned_data
        title = data.get('title')
        qs = Articles.objects.filter(title__icontains=title)
        print(qs)
        if qs.exists():
            self.add_error("title", f"\"{title}\" title already exists!")
        return data


class ArticleformOld(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

    def clean_title(self):
        cleaned_data = self.cleaned_data
        print("cleaned_data", cleaned_data)
        title = cleaned_data.get('title')
        if title.lower().strip() == 'article2':
            raise forms.ValidationError("This title is taken!")
        print("title", title)
        return title

    def clean(self):
        cleaned_data = self.cleaned_data
        print("All data", cleaned_data)
        return cleaned_data