from django.contrib.auth.models import BaseUserManager
#پروفایل ادمین

class UserManager(BaseUserManager):
    def create_user(self, Phone, password=None):

        if not Phone:
            raise ValueError("Users must have an Phone number")

        user = self.model(
            Phone=self.normalize_email(Phone),
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

#پروفایل کاربر سوپر

    def create_superuser(self, Phone, password=None):

        user = self.create_user(
            Phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
