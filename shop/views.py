from django.db import transaction
from django.db.models import F, Avg
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from analysis.forms import RatingForm
from analysis.models import ProductStatistic, RatingProduct, RatingStar
from cart.forms import CartAddProductForm
from .models import Category, Product
from .utils import get_client_ip


class ServiceProduct:
    def get_categories(self):
        return Category.objects.all()

    def get_rating(self):
        return RatingStar.objects.all()

    def set_popular_product(self, request, obj):
        with transaction.atomic():
            counter, created = ProductStatistic.objects.get_or_create(product_id=obj.id)
            counter.ip_client = get_client_ip(request)
            counter.count_views = F('count_views') + 1
            if ProductStatistic.objects.get(product_id=obj.id).ip_client == get_client_ip(request):
                pass
            else:
                counter.save()


class ProductView(ServiceProduct, ListView):
    model = Product
    queryset = Product.objects.filter(available=True)
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        queryset = Product.objects.filter(available=True)
        if self.request.GET.getlist('category'):
            queryset = Product.objects.filter(
                category__slug__in=self.request.GET.getlist('category'), available=True
            )
        return queryset


class ProductDetailView1(ServiceProduct, DetailView):
    model = Product
    slug_field = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['cart_product_form'] = CartAddProductForm()

        ServiceProduct().set_popular_product(request=self.request, obj=self.object)
        ratingstar = RatingProduct.objects.filter(product=self.object.id)
        if ratingstar:
            context['rating_avg'] = str(int(ratingstar.aggregate(Avg('star_id'))['star_id__avg']))
        else:
            context['rating_avg'] = ""
        return context


class Search(ServiceProduct, ListView):
    paginate_by = 3
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get('search'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search')
        return context


def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cart_product_form = CartAddProductForm()
    popular_products = ProductStatistic.objects.order_by('-count_views')[:5]
    star_rating = RatingStar.objects.all()

    return render(request, 'shop/home.html', {'categories': categories,
                                              'products': products,
                                              'cart_product_form': cart_product_form,
                                              'popular_products': popular_products,
                                              'star_rating': star_rating,
                                              })
