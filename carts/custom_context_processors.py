from .models import Cart


def cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return {'cart_counter': cart.cart_items.count()}
    return {'cart_counter': 0}
