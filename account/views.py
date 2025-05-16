from django.contrib.auth import authenticate , login, logout
from django.shortcuts import render , redirect
from django.views import View
from .forms import LoginForm,RegisterForm

class UserLogin(View):
    @staticmethod
    def get (request):
        form = LoginForm()
        return render(request,'login.html',{'form':form})

    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            valid = form.cleaned_data
            login_user = authenticate(username=valid['phone'],password=valid['password'])
            if login_user is not None:
                login(request,login_user)
                return redirect('Home:home')
            else:
                form.add_error("phone", "اطلاعات وارد شده صحیح نمی باشد ")
        else:
            form.add_error("phone","لطفا دوباره بررسی کنید اطلاعات وارد شده صحیح نمی باشد")

        return render(request,'login.html',{'form':form})

class UserRegister(View):
    def get (self,request):
        form = RegisterForm()
        return render(request, 'register.html', {'form':form})