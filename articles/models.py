from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from .utils import slugify_instance_title
from django.urls import reverse
from django.db.models import Q

User = settings.AUTH_USER_MODEL

class ArticlesQuerySet(models.QuerySet):
    def search(self, query=None):
        if query is None or query == "":
            return self.get_queryset().none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query)
        return self.filter(lookups)

class ArticlesManager(models.Manager):
    def get_queryset(self):
        return ArticlesQuerySet(self.model, using=self._db)
    
    def search(self, query=None):  
        # return Articles.objects.filter(lookups)
        return self.get_queryset().search(query=query)

class Articles(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateField(auto_now_add=False, auto_now=False, null=True, blank=True)
    objects = ArticlesManager()

    def get_real_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})

    # def get_search_url(self):
    #         return reverse("article:search", kwargs={})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slugify_instance_title(instance, save=False)

pre_save.connect(article_pre_save, sender=Articles)

def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slugify_instance_title(instance, save=True)

post_save.connect(article_post_save, sender=Articles)