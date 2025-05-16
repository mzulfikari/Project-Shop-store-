from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import django_filters
from django_filters.views import FilterView
from carts.models import Cart
from .models import Product, MainCategory
from carts.forms import CartItemForm
from configs.sepandyar_webAPI import get_product

# class ProductFilter(django_filters.FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'name': ['exact', 'icontains'],
#             'brand': ['exact', 'icontains'],
#             'category': ['exact'],
#             'colors': ['exact'],
#             'price': ['gte', 'lte'],
#             'discount': ['gte', 'lte'],
#             'avg_rate': ['gte', 'lte'],
#             'created': ['gte', 'lte'],
#         }


# /products/?name=product1&brand__icontains=brand1&price__gte=1000&price__lte=5000&ordering=price


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')
    brand = django_filters.CharFilter(field_name='brand', lookup_expr='contains')
    # category = django_filters.ModelMultipleChoiceFilter(queryset=MainCategory.objects.all())
    category = django_filters.CharFilter(method='filter_by_category_name_or_parent')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='حداقل قیمت')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='حداکثر قیمت')

    order_by = django_filters.OrderingFilter(
        fields=(
            ('created', 'created'),
            ('price', 'price'),
            ('discount', 'discount'),
            # ('avg_rate', 'avg_rate'),
        )
    )

    class Meta:
        model = Product
        fields = ['name', 'brand', 'category', 'price_min', 'price_max']

    def filter_by_category_name_or_parent(self, queryset, name, value):
        return queryset.filter(
            Q(category__name__iexact=value) | Q(category__parent__name__iexact=value)
        )


class HomeView(TemplateView):
    template_name = 'products/home.html'

    def get(self, request, *args, **kwargs):
        messages.warning(request, 'سایت در مرحله تست و ارزیابی می باشد ، لطفا از خرید و ثبت سفارش خودداری فرمایید.')
        return super().get(request, *args, **kwargs)


class ProductListView(FilterView):
    model = Product
    template_name = 'products/all-products.html'
    context_object_name = 'products'
    paginate_by = 20
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.available.all().order_by('-id')

    def get_queryset(self):
        queryset = Product.available.all().order_by('-created')
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        parent_category = self.request.GET.get('category')
        if parent_category:
            sub_category = MainCategory.objects.filter(parent__name=parent_category)
            context['suggest_categories'] = sub_category
        return context


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cart, _ = Cart.objects.get_or_create(user=self.request.user)
        # for cart_item in cart.cart_items.all():
        #     if cart_item.product.id == self.get_object().id:
        #         context['cart_item'] = cart_item
        #     else:
        #         context['cart_item'] = None

        context['form'] = CartItemForm()
        # try:
        #     context['quantity'] = int(get_product(self.get_object().code)['Quantity'])
        # except Exception as e:
        #     print(str(e))
        #     context['quantity'] = 1
        return context
