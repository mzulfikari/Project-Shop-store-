from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MaxValueValidator, MinValueValidator
import django_jalali.db.models as jmodels
# from product.categories import MainCategory, Brand
from .managers import AvailableManager, SpecialOfferManager


class Base(models.Model):
    name = models.CharField(_('نام'), max_length=40, unique=True)
    image = models.ImageField(_('عکس'), upload_to='category-and-brands/', null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(Base):
    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برند ها"


class MainCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(_('نام'), max_length=40, db_index=True)
    image = models.ImageField(_('عکس'), upload_to='category-and-brands/', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='زیر دسته')

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی"

    def __str__(self):
        return self.name


class SpecialCategory(Base):
    class Meta:
        verbose_name = "دسته بندی مناسبتی"
        verbose_name_plural = "دسته بندی مناسبتی"


# class Color(models.Model):
#     name = models.CharField(_('رنگ'), max_length=30)
#     code = models.CharField(_('کد رنگ'), max_length=10, default='#FF0000', null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'رنگ'
#         verbose_name_plural = 'رنگ ها'
#
#     def __str__(self):
#         return self.name
#
#
# class Size(models.Model):
#     value = models.CharField(_('سایز'), max_length=30, unique=True)
#
#     class Meta:
#         verbose_name = 'سایز'
#         verbose_name_plural = 'سایز ها'
#
#     def __str__(self):
#         return self.value


# class ProductImage(models.Model):
#     product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE, verbose_name='محصول')
#     image = models.ImageField(_('عکس محصول'), upload_to='products/')
#
#     def __str__(self):
#         return self.image.name


class ProductFeature(models.Model):
    product = models.ForeignKey('Product', related_name='features', on_delete=models.CASCADE, verbose_name='محصول')
    key = models.CharField(_('موضوع'), max_length=100)
    value = models.CharField(_('مقدار'), max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(_('کد محصول'), max_length=15, null=True, blank=True, unique=True, db_index=True)
    cover_image = models.ImageField(_('عکس کاور'), upload_to='cover_images/', null=True, blank=True)
    name = models.CharField(_('نام محصول'), max_length=200, db_index=True)

    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.SET_NULL,
                              null=True, blank=True, verbose_name='برند')

    category = models.ForeignKey(MainCategory, related_name='products', on_delete=models.SET_NULL,
                                 null=True, blank=True, verbose_name='دسته بندی اصلی')

    # colors = models.ManyToManyField(Color, related_name='products', blank=True, verbose_name='رنگ')
    # sizes = models.ManyToManyField(Size, related_name='products', blank=True, verbose_name='سایز')
    price = models.PositiveIntegerField(_('قیمت'))
    discount = models.PositiveSmallIntegerField(_('تخفیف (%)'), default=0)
    # quantity = models.PositiveIntegerField(_('تعداد'), default=1)
    unit_type = models.PositiveSmallIntegerField(_('واحد'), default=1, choices=[(1, 'عدد'), (2, 'کیلو')])
    quantity = models.DecimalField(_('تعداد'), default=1.0, max_digits=12, decimal_places=7)

    # avg_rate = models.DecimalField(_('امتیاز'), validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],default=0,
    #                                decimal_places=1, max_digits=2)

    description = models.TextField(_('توضیحات'), null=True, blank=True)
    # is_in_special_category = models.BooleanField(_('فعال در مناسبت'), default=False)
    active = models.BooleanField(_('فعال'), default=True)

    objects = models.Manager()
    # in_special_category = SpecialCategory()
    # special_offer = SpecialOfferManager()
    available = AvailableManager()

    created = models.DateField(_('تاریخ ایجاد'), auto_now_add=True)
    updated = models.DateField(_('تاریخ آپدیت'), auto_now=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return f'{self.name[:15]}... - کد: {self.code}'

    @property
    def discounted_price(self):
        if self.discount:
            return int(self.price * (1 - (self.discount / 100)))
        return self.price
