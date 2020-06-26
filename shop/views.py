from django.db import transaction
from django.db.models import F, Avg
from django.shortcuts import render, get_object_or_404

from analysis.forms import RatingForm
from analysis.models import ProductStatistic, RatingProduct
from cart.forms import CartAddProductForm
from .models import Category, Product
from .utils import get_client_ip


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    popular_products = ProductStatistic.objects.order_by('-count_views')[:5]

    return render(request, 'shop/home.html', {'categories': categories,
                                              'products': products,
                                              'cart_product_form': cart_product_form,
                                              'popular_products': popular_products,
                                              })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {'category': category,
                                                      'categories': categories,
                                                      'products': products
                                                      })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    rating = RatingForm()
    ratingstar = RatingProduct.objects.filter(product=id)
    rating_avg = str(int(ratingstar.aggregate(Avg('star_id'))['star_id__avg']))

    with transaction.atomic():
        counter, created = ProductStatistic.objects.get_or_create(product=product)
        counter.ip_client = get_client_ip(request)
        counter.count_views = F('count_views') + 1
        if ProductStatistic.objects.get(product=product).ip_client == get_client_ip(request):
            pass
        else:
            counter.save()

    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form,
                                                        'rating': rating,
                                                        'rating_avg': rating_avg,
                                                        })
