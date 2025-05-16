from django.core.management.base import BaseCommand
from django.utils import timezone
from jdatetime import datetime, timedelta
from carts.models import Cart


class Command(BaseCommand):
    help = 'Delete carts that are older than one month'

    def handle(self, *args, **kwargs):
        one_month_ago = timezone.now() - timedelta(weeks=4)

        carts_to_delete = Cart.objects.filter(
            created__lte=one_month_ago,
        )

        count, _ = carts_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} orders.'))
