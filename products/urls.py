from django.urls import path,include
from django.contrib.auth.views import LogoutView
from .views import HomeView, ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
