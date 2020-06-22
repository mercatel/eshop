from decimal import Decimal
from django.conf import settings

from coupons.models import Coupon
from shop.models import Product


class Cart(object):

    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'discount_price': str(product.get_price_with_discount()),
                                     'price': str(product.price),
                                     }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
            cart[str(product.id)]['price'] = product.price
        for item in cart.values():
            # Сумма без скидки (цена * кол-во)
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['discount_price'] = Decimal(item['discount_price'])
            # Сумма с учетом скидки (цена с учетом скидки * кол-во)
            total_discount_price = item['discount_price'] * item['quantity']

            if item['discount_price'] == item['price']:
                if self.coupon:
                    count_discount = Decimal(self.coupon.discount / 100) * total_discount_price
                    item['total_discount_price'] = total_discount_price - count_discount
                else:
                    item['total_discount_price'] = item['discount_price'] * item['quantity']
            else:
                item['total_discount_price'] = item['discount_price'] * item['quantity']
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(
            item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()

    # Логика корзины
    # ----------------------
    def get_total_price(self):
        # Сумма всех товаров в корзине по исходным ценам
        res = 0
        for item in self.cart.values():
            res += Decimal(item['price']) * item['quantity']
        return res

    # Логика скидок, акций, купонов и прочее
    # ----------------------------
    @property
    def coupon(self):
        # получение обьекта купона по фильтрам
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_total_price_after_discount(self):
        # получение Суммы с учетом всех скидок
        try:
            return self.get_total_price() - self.get_total_discount()
        except:
            res = 0
            for item in self.cart.values():
                res += Decimal(item['discount_price']) * Decimal(item['quantity'])
            return res

    def get_total_discount(self):
        # возвращает сумму скидки всех товаров в корзине
        res = 0
        for item in self.cart.values():
            res += item['total_discount_price']

        return self.get_total_price() - res
