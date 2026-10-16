from django.test import TestCase
from .models import Articles
from django.utils.text import slugify
from .utils import slugify_instance_title

class ArticlesTestCase(TestCase):
    def setUp(self):
        self.number_of_articles = 15
        for i in range (0, self.number_of_articles):
            Articles.objects.create(title="hello world", content="something is there")
    
    def test_queryset_exists(self):
        qs = Articles.objects.all()
        self.assertTrue(qs.exists())

    def test_queryset_count(self):
        qs = Articles.objects.all()
        self.assertEqual(qs.count(), self.number_of_articles)

    def test_custom_name_slug(self):
        obj = Articles.objects.all().order_by("id").first()
        slug = obj.slug
        title = obj.title
        title_slug = slugify(title)
        self.assertEqual(slug, title_slug)

    def test_slug_name_slug(self):
        qs = Articles.objects.all().exclude(slug__iexact="hello-world")
        for obj in qs:
            slug = obj.slug
            title = obj.title
            title_slug = slugify(title)
            self.assertNotEqual(slug, title_slug)

    def test_slugify_instance_title(self):
        obj = Articles.objects.all().last()

        slugs = []
        for i in range(0, 5):
            instance = slugify_instance_title(obj, save=False)
            slugs.append(instance.slug)

        unique_slugs = list(set(slugs))
        self.assertEqual(len(slugs), len(unique_slugs))
