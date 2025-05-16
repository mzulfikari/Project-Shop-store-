from django.db import models
from products.models import Product
import django_jalali.db.models as jmodels
from django.utils.translation import gettext as _
from accounts.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='cart')
    send_price = models.PositiveIntegerField(_('هزینه ی ارسال'), default=0, help_text='به تومان')

    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد خرید"

    def __str__(self):
        return f'سبد برای : {self.user}'

    def calculate_total_price(self):
        return sum(cart.cart_item_price() for cart in self.cart_items.all())

    def calculate_total_discounted_price(self):
        return sum(cart.cart_item_discounted_price() for cart in self.cart_items.all()) + self.send_price

    def calculate_total_discount(self):
        return sum(cart.cart_item_discount() for cart in self.cart_items.all())

    def total_quantity(self):
        return self.cart_items.all().count()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items", verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True, verbose_name='محصول')
    quantity = models.DecimalField(_('تعداد'), default=1.0, max_digits=12, decimal_places=7)

    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم سبد خرید"

    def __str__(self):
        return f"{self.quantity} عدد از {self.product}"

    def cart_item_price(self):
        return int(self.product.price * self.quantity)

    def cart_item_discounted_price(self):
        return int(self.product.discounted_price * self.quantity)

    def cart_item_discount(self):
        return (self.product.price * self.quantity) - (self.product.discounted_price * self.quantity)

    @property
    def rounded_quantity(self):
        return int(self.quantity) if self.product.unit_type == 1 else round(self.quantity, 1)
