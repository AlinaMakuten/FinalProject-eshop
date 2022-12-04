from django.db import models
from django.urls import reverse


class Category(models.Model):
    category_name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(max_length = 1000, blank=True)
    category_image = models.ImageField(upload_to='photos/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def get_all_url(self):
        return reverse('all_products')

    def __str__(self):
        return self.category_name