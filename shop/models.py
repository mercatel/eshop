from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='category')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=480, db_index=True)
    slug = models.SlugField(max_length=480, db_index=True)
    description = models.TextField(blank=True)
    promo_action = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    def get_price_with_discount(self):
        if self.promoaction.all():
            result = self.price - ((self.price / 100) * self.promoaction.get().discount)
        else:
            result = self.price
        return result


def get_product_deirectory(instance, filename):
    return "/".join(['products', instance.product.name, filename])


class ImageProduct(models.Model):
    product = models.ForeignKey(Product, related_name='imageproducts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_product_deirectory)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('product',)
        verbose_name = 'Изображение продукта'
        verbose_name_plural = 'Изображения продукта'


class PromoAction(models.Model):
    name = models.CharField(max_length=48)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тип Акции'
        verbose_name_plural = 'Тип Акции'

    def __str__(self):
        return "{}".format(self.name)


class PromoActionProduct(models.Model):
    name = models.ForeignKey(PromoAction, related_name='type_promo_action', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='promoaction', on_delete=models.CASCADE)
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('product',)
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'



