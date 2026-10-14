from django.utils.text import slugify

def slugify_instance_title(instance, count=1, original_slug=None, save=False, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
        original_slug = slug

    model_class = instance.__class__
    qs = model_class.objects.filter(slug=slug).exclude(id=instance.id)

    if qs.exists():
        count = count + 1;
        # rand_int = random.randint(300_000, 500_000)
        slug = f"{original_slug}-{count}"
        return slugify_instance_title(instance, count=count, original_slug=original_slug, save=save, new_slug = slug)
    
    instance.slug = slug
    if save:
        instance.save()