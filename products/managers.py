from django.db import models


class AvailableManager(models.Manager):
    def get_queryset(self):
        return super(AvailableManager, self).get_queryset().filter(active=True, price__gt=1, quantity__gte=1)


class SpecialCategoryManager(models.Manager):
    def get_queryset(self):
        return super(SpecialCategoryManager, self).get_queryset().filter(active=True,
                                                                         quantity__gte=1,
                                                                         is_in_special_category=True)


class SpecialOfferManager(models.Manager):
    def get_queryset(self):
        return super(SpecialOfferManager, self).get_queryset().filter(active=True,
                                                                      quantity__gte=1,
                                                                      discount__gte=20)
