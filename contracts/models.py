from django.conf import settings
from django.db import models

from config.models import BasedModel
from properties.models import Unit


class TenancyContract(BasedModel):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenancy_contracts')
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenancy_contracts')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_contracts')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=False)
    rent_agreed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.tenant} - {self.unit} ({self.start_date} to {self.end_date or 'present'})"
