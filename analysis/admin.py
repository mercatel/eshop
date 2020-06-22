from django.contrib import admin

# Register your models here.
from analysis.models import ProductStatistic


# class ProductStatisticAdmin(admin.ModelAdmin):
#     list_display = ('__str__', 'date', 'views')  # отображаемые поля в админке
#     search_fields = ('__str__',)  # поле, по которому производится поиск
#
#
# admin.site.register(ProductStatistic)
# admin.site.register(ProductStatistic, ProductStatisticAdmin)
