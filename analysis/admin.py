from django.contrib import admin

# Register your models here.
from analysis.models import ProductStatistic, RatingStar


@admin.register(ProductStatistic)
class ProductStatisticAdmin(admin.ModelAdmin):
    list_display = ['product', 'date', 'count_views']  # отображаемые поля в админке
    search_fields = ('product',)  # поле, по которому производится поиск


admin.site.register(RatingStar)
