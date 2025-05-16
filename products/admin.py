from django.contrib import admin
from django.utils.html import format_html
# from .categories import Brand, MainCategory, SpecialCategory
from .models import ProductFeature, Product, Brand, MainCategory, SpecialCategory
from django.forms import CheckboxSelectMultiple
from django.db import models


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', )
    search_fields = ('name', )
    list_filter = ('name', )

    fieldsets = (
        (None, {'fields': ('name',)}),
        (None, {'fields': ('image',)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}"style="width:45px;height:45px;"/>', obj.image.url
            )
        return "-"


@admin.register(MainCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'image_tag', )
    search_fields = ('id', 'name', )
    autocomplete_fields = ('parent', )
    list_display_links = ('id', 'name')
    # list_filter = ('name', )

    fieldsets = (
        (None, {'fields': ('parent', 'name',)}),
        (None, {'fields': ('image',)}),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}"style="width:45px;height:45px;"/>', obj.image.url
            )
        return "-"

    # def get_model_perms(self, request):
    #     """
    #     Return empty perms dict thus hiding the model from admin index.
    #     """
    #     return {}


# admin.site.register(Brand, CategoryAdmin)
# admin.site.register(MainCategory, CategoryAdmin)
# admin.site.register(SpecialCategory, CategoryAdmin)


# class ManyToManyAdmin(admin.ModelAdmin):
#     def get_model_perms(self, request):
#         """
#         Return empty perms dict thus hiding the model from admin index.
#         """
#         return {}


# admin.site.register(Color, ManyToManyAdmin)
# admin.site.register(Color, ManyToManyAdmin)

# admin.site.register(Color)
# admin.site.register(Size)

# admin.site.register(ProductImage)
# admin.site.register(ProductFeature)

# =============================================================================================


# class ProductImageInline(admin.TabularInline):
#     model = ProductImage
#     extra = 2
#
#
# class ProductFeatureInline(admin.TabularInline):
#     model = ProductFeature
#     extra = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'price', 'discount', 'quantity', 'category', 'active', 'created')
    list_filter = ('category', 'brand', 'active', 'created')
    search_fields = ('id', 'code', 'name', 'description')
    autocomplete_fields = ('category', 'brand')
    list_display_links = (('id', 'code', 'name'))
    ordering = ['-created', ]
    # inlines = [ProductImageInline, ProductFeatureInline]

    # formfield_overrides = {
    #     models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    # }

    # def get_queryset(self, request):
    #     return Product.objects.all()

    # @admin.display(description="شماره تلفن")
    # def phone_number(self, obj):
    #     return obj.user.phone_number

    # def is_active(self, obj):
    #     return obj.is_verified
    # is_active.boolean = True
    # is_active.short_description = 'فعال'
    #
    # def special_category(self, obj):
    #     return obj.is_in_special_category
    # special_category.boolean = True
    # special_category.short_description = 'در دسته بندی مناسبتی'
