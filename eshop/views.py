from django.shortcuts import render
from products.models import Product

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    context = {
        'products': products,
    }
    return render(request, 'home.html', context=context)