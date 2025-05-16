from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from account.models import User
from django.core import validators

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["Phone", "last_name"]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("گذرواژه ها مطابقت ندارند")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ["Phone", "password", "first_name","last_name", "is_active", "is_admin"]

class LoginForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center'}))

    def clean_Phone(self):
        Phone = self.cleaned_data.get('phone')
        if len(Phone) > 11:
            raise ValidationError('تلفن وارد شده صحیح نمی باشد',code='invalid Phone' )
        return Phone

class RegisterForm(forms.ModelForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full drop-shadow-lg outline-none rounded-2xl py-2 text-center'})
     ,validators=[validators.MaxValueValidator(11)])