from django.contrib import admin
from .models import User


class RoleFilter(admin.SimpleListFilter):
    title = 'role'
    parameter_name = 'role'

    def lookups(self, request, model_admin):
        return User.USER_ROLES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(role=self.value())
        return queryset
