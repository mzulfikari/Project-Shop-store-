from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, DeleteView, RedirectView
from products.models import Product
from .forms import CartItemForm
from .models import Cart, CartItem
from configs.sepandyar_webAPI import get_product
from decimal import Decimal

def get_quantity_from_api(product_code):
    try:
        get_product_from_api = get_product(product_code)

        if get_product_from_api is not None:
            product_quantity = get_product_from_api['Quantity']
            return product_quantity

        return 1

    except Exception as e:
        print(str(e))

        try:
            return Product.objects.get(code=product_code).quantity
        except Exception as e:
            print(str(e))
            return 1


class CartItemCreateUpdateView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        return redirect('products:home')

    def post(self, request, *args, **kwargs):
        # product_id = request.POST.get('product_id')
        # product = get_object_or_404(Product, id=product_id)

        form = CartItemForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quantity = cd['quantity']
            product = cd['product']
            product_quantity = get_quantity_from_api(product.code)

            if product_quantity < float(quantity):
                messages.error(request, 'تعداد درخواستی از مانده انبار بیشتر می باشد!')
                return redirect(request.META.get('HTTP_REFERER', 'carts:all'))

            try:
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
                cart_item, created = CartItem.objects.update_or_create(cart=cart, product=product)

                cart_item.quantity = quantity
                cart_item.save()

                messages.success(self.request, 'محصول به سبد خرید اضافه شد!')
                return redirect(request.META.get('HTTP_REFERER', 'carts:all'))

            except Exception as e:
                messages.error(self.request, 'خطا در انجام درخواست!')

        return redirect(request.META.get('HTTP_REFERER', 'carts:all'))
        # return HttpResponse("اطلاعات ارسال شده نامعتبر است!", status=400)
        # return super().post(request, *args, **kwargs)

# class CartItemCreateUpdateView(LoginRequiredMixin, CreateView):
#     model = CartItem
#     form_class = CartItemForm
#     template_name = 'cart/cart_item_form.html'
#     success_url = reverse_lazy('carts:all')
#
#     def form_valid(self, form):
#         product = form.cleaned_data['product']
#         quantity = form.cleaned_data['quantity']
#         color = form.cleaned_data['color']
#
#         if product.quantity < quantity:
#             messages.error(self.request, 'موجودی کافی نیست.')
#             return self.form_invalid(form)
#
#         try:
#             cart, created = Cart.objects.get_or_create(user=self.request.user)
#             cart_item, created = CartItem.objects.update_or_create(
#                 cart=cart,
#                 product=product,
#                 color=color,
#                 defaults={'quantity': quantity}
#             )
#             messages.success(self.request, 'سبد خرید با موفقیت به‌روز شد.')
#         except Exception as e:
#             messages.error(self.request, 'خطایی در به‌روزرسانی سبد خرید رخ داد.')
#             return self.form_invalid(form)
#
#         return super().form_valid(form)


class CartDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart_id = kwargs.get('pk')
        cart_item = get_object_or_404(CartItem, pk=cart_id)
        cart_item.delete()

        return redirect('carts:all')

# class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = CartItem
#     success_url = reverse_lazy('carts:all')
#
#     def test_func(self):
#         cart_item = self.get_object()
#         return cart_item.cart.user == self.request.user


class CartList(LoginRequiredMixin, TemplateView):
    template_name = 'carts/my-carts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        context['carts'] = cart.cart_items.all()
        context['cart'] = cart
        return context

# class CartList(LoginRequiredMixin, ListView):
#     model = CartItem
#     template_name = 'cart/cart_list.html'
#     context_object_name = 'cart_items'
#
#     def get_queryset(self):
#         cart, _ = Cart.objects.get_or_create(user=self.request.user)
#         return CartItem.objects.filter(cart=cart)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['cart'] = self.request.user.cart
#         return context


class UpdateCartItemQuantityView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart_item_id = request.POST.get('cartitem_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        product = cart_item.product
        product_quantity = get_quantity_from_api(product.code)

        if action == 'increase':
            increment = Decimal('1.0') if product.unit_type == 1 else Decimal('0.1')
            cart_item.quantity += increment

            if product_quantity < cart_item.quantity:
                messages.error(request, 'تعداد درخواستی از مانده انبار بیشتر می باشد!')
                return redirect(request.META.get('HTTP_REFERER', 'carts:all'))

        elif action == 'decrease':
            increment = Decimal('1.0') if product.unit_type == 1 else Decimal('0.1')
            if cart_item.quantity >= 0.1:
                cart_item.quantity -= increment
                if cart_item.quantity <= 0:
                    cart_item.delete()
                    # messages.error(request, 'تعداد نمیتواند کمتر از 1 باشد!')
                    return redirect(request.META.get('HTTP_REFERER', 'carts:all'))

        cart_item.save()

        # return redirect('carts:all')
        return redirect(request.META.get('HTTP_REFERER', 'carts:all'))