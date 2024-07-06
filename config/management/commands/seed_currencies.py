from django.core.management.base import BaseCommand

from properties.models import Currency


class Command(BaseCommand):
    help = 'Seed database with initial currency data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data.')

        currencies = [
            {'code': 'USD', 'name': 'US Dollar'},
            {'code': 'EUR', 'name': 'Euro'},
            {'code': 'GBP', 'name': 'British Pound'},
            {'code': 'PKR', 'name': 'Pakistani Rupee'},
        ]

        for currency in currencies:
            Currency.objects.get_or_create(code=currency['code'], defaults={'name': currency['name']})

        self.stdout.write('Data seeded successfully.')
