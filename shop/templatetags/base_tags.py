from django import template
from ..models import *
# from account.models import MyUser
from django.db.models import Q

register = template.Library()



@register.inclusion_tag("shop/partials/category-menu.html")
def category_menu():
    return {
            'allCategory': Category.objects.filter(Q(status='p') | Q(status='d')).only('slug', 'title', 'parent')
        }

@register.inclusion_tag("shop/partials/new-products.html")
def new_products():
    return {
            'newProducts': Product.objects.filter(is_active=True).order_by('-created')[:5]
        }

