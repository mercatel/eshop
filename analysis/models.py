from django.db import models

# Create your models here.
from django.utils import timezone

from shop.models import Product


class ProductStatistic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    date = models.DateField(default=timezone.now)
    count_views = models.IntegerField(default=0)
    ip_client = models.GenericIPAddressField(default="0")

    def __str__(self):
        return self.product.name


class RatingStar(models.Model):
    value = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']

    def __str__(self):
        return "{}".format(self.value)


class RatingProduct(models.Model):
    ip = models.GenericIPAddressField(default=0)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.star, self.product)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        ordering = ['-star']
