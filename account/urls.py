from django.urls import path
from .import views

# نام اپ کاربران
app_name="account"

urlpatterns = [
    path('login',views.UserLogin.as_view(), name='Login-user'),
    path('register',views.UserRegister.as_view(), name='Register-user'),

]