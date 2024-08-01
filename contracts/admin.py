from django.contrib import admin

from .models import Message, TenancyContract

admin.site.register(TenancyContract)
admin.site.register(Message)
