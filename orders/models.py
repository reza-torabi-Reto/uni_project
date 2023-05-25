from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator,MaxValueValidator
from coupons.models import Coupon


class Order(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    email = models.EmailField(verbose_name='رایانامه')
    address = models.CharField(max_length=250, verbose_name='نشانی')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')
    city = models.CharField(max_length=100, verbose_name='شهر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ سفارش')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')
    paid = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    braintree_id = models.CharField(max_length=150, blank=True, verbose_name='شماره پرداخت')
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='بن پرداخت')
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)],  verbose_name='تخفیف')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal(100))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity