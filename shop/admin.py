from django.contrib import admin
from .models import Category, Product, ImageProduct, PromoActionProduct, PromoAction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    raw_id_fields = ['product']
    extra = 1


class PromoActionProductInline(admin.TabularInline):
    model = PromoActionProduct
    raw_id_fields = ['product']
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'promo_action', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'promo_action', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PromoActionProductInline, ImageProductInline]


admin.site.register(PromoAction)
