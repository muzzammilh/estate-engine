from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse

from config.models import BasedModel


class Country(BasedModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class State(BasedModel):
    country = models.ForeignKey(Country, related_name='states', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(BasedModel):
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SubLocality(BasedModel):
    city = models.ForeignKey(City, related_name='sub_localities', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Property(BasedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    sub_locality = models.ForeignKey(SubLocality, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    square_feet = models.PositiveIntegerField()
    is_leased = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
    images = GenericRelation('gallery.Image')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        self.images.all().delete()
        super().delete(*args, **kwargs)


class Unit(BasedModel):
    property = models.ForeignKey(Property, related_name='units', on_delete=models.CASCADE)
    unit_number = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    num_beds = models.PositiveIntegerField()
    num_bathrooms = models.PositiveIntegerField()
    num_kitchens = models.PositiveIntegerField()
    num_living_rooms = models.PositiveIntegerField()
    num_stores = models.PositiveIntegerField()
    images = GenericRelation('gallery.Image')
    is_available_for_rent = models.BooleanField(default=False)
    rent_per_month = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Unit {self.unit_number} in {self.property.name}"

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.property.pk})

    def delete(self, *args, **kwargs):
        self.images.all().delete()
        super().delete(*args, **kwargs)


class Document(BasedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='documents')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = GenericRelation('gallery.Image')

    def __str__(self):
        return f"Images for Unit {self.unit.unit_number}"
