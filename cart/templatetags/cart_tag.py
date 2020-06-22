from django import template

from cart.cart import Cart

register = template.Library()


@register.simple_tag()
def get_cart():
    return {'cart': Cart}
