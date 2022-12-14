from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg, Count


class Product(models.Model):
    author = models.CharField(max_length=100)
    book_title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    product_description = models.TextField(max_length=4600, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def average_review(self):
        reviews = ReviewRating.objects.filter(product = self, status=True).aggregate(average=Avg('rating'))
        avg=0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def __str__(self):
        return self.book_title


class VariationManager(models.Manager):
    def format(self):
        return super(VariationManager, self).filter(variation_category='format', is_active=True)


variation_category_choice = (
    ('format', 'format'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=50, choices=variation_category_choice)
    variation_value = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value



class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    review=models.TextField(max_length=600, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=25, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updatedt_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.review


