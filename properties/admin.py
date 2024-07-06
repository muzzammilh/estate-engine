# properties/admin.py

from django.contrib import admin

from .models import City, Country, Currency, Property, State, SubLocality, Unit

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(SubLocality)
admin.site.register(Property)
admin.site.register(Unit)
admin.site.register(Currency)
