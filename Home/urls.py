from django.urls import path
from .import views

# نام اپ اصلی
app_name="Home"

urlpatterns = [
    path('',views.Home.as_view(), name='home'),

]