# properties/admin.py

from django.contrib import admin

from .models import (City, Country, Property, PropertyImage, State,
                     SubLocality, Unit, UnitImage)

admin.site.register(Country)
admin.site.register(State)
admin.site.register(City)
admin.site.register(SubLocality)
admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(Unit)
admin.site.register(UnitImage)
