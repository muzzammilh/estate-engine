from django.core.management.base import BaseCommand

from properties.models import City, Country, State, SubLocality


class Command(BaseCommand):
    help = 'Seed database with initial location data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data.')

        # Add Country
        pakistan = Country.objects.get_or_create(name='Pakistan')[0]

        # Add States
        sindh = State.objects.get_or_create(name='Sindh', country=pakistan)[0]
        punjab = State.objects.get_or_create(name='Punjab', country=pakistan)[0]

        # Add Cities
        karachi = City.objects.get_or_create(name='Karachi', state=sindh)[0]
        lahore = City.objects.get_or_create(name='Lahore', state=punjab)[0]
        islamabad = City.objects.get_or_create(name='Islamabad', state=punjab)[0]
        rawalpindi = City.objects.get_or_create(name='Rawalpindi', state=punjab)[0]

        # Add Sub Localities
        SubLocality.objects.get_or_create(name='Clifton', city=karachi)
        SubLocality.objects.get_or_create(name='Gulshan-e-Iqbal', city=karachi)
        SubLocality.objects.get_or_create(name='DHA', city=lahore)
        SubLocality.objects.get_or_create(name='Bahria Town', city=islamabad)
        SubLocality.objects.get_or_create(name='Satellite Town', city=rawalpindi)

        self.stdout.write('Data seeded successfully.')
