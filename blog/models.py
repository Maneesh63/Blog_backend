from django.db import models
from django.utils.text import slugify
from uuid import uuid4

class Datetime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(models.Model):
    category_id = models.UUIDField(
        default=uuid4,
        editable=False,
        unique=True,
        primary_key=True
    )
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blogs(Datetime):
    blog_id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    content = models.JSONField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='blogs') #set to null when category is deleted

    def __str__(self):
        return self.title
    