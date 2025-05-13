from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User
from account.forms import UserChangeForm, UserCreationForm

class UserAdmin(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ["email", "verification_time", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["verification_time"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["Phone", "verification_time", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["Phone"]
    ordering = ["Phone"]
    filter_horizontal = []



admin.site.register(User, UserAdmin)
admin.site.unregister(Group)