from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    context = {'products': Product.objects.all()}
    return render(request, 'catalog/home.html', context)


def contacts(request):
    return render(request, 'catalog/contacts.html')


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)
