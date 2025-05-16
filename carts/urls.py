from django.urls import path
from .views import CartItemCreateUpdateView, UpdateCartItemQuantityView, CartDeleteView, CartList

app_name = 'carts'
urlpatterns = [
    path('', CartItemCreateUpdateView.as_view(), name='add'),

    path('update/', UpdateCartItemQuantityView.as_view(), name='update_cartitem'),

    path('delete/<int:pk>/', CartDeleteView.as_view(), name='remove'),
    path('my-carts/', CartList.as_view(), name='all'),

]