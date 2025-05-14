from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User
from account.forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ["Phone","first_name","last_name", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["Phone", "password"]}),
        ("اطلاعات فردی", {"fields": ["first_name","last_name"]}),
        ("وضعیت ادمین", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["Phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["Phone"]
    ordering = ["Phone"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)