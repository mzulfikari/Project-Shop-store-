from .models import MainCategory, Brand, Product


def category(request):
    all_products = Product.available.all()
    # most_discount = all_products.order_by('-discount').exclude(discount=0)[:10]
    new_products = all_products.order_by('-id')[:10]
    brands = Brand.objects.all()[:10]

    category = MainCategory.objects.filter(parent__isnull=True)
    sub_category = MainCategory.objects.filter(parent__isnull=False)
    all_categories = {}
    for cat in category:
        all_categories[cat] = []
        for s_cat in sub_category:
            if s_cat.parent.name == cat.name:
                all_categories[cat] += [s_cat, ]
    return {'all_categories': all_categories,
            'brands': brands,
            'new_products': new_products,
            # 'most_discount': most_discount
            }
