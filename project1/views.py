from django.http import HttpResponse
from articles.models import Articles
from django.template.loader import render_to_string



def home_view(requests):
    obj1 = Articles.objects.get(id=1)
    objects = Articles.objects.all()
    context = {
        'title': obj1.title,
        'id': obj1.id,
        'content': obj1.content,
        'object_list': objects
    }
    HTML_STRING = render_to_string("home-view.html", context=context)
    return HttpResponse(HTML_STRING)