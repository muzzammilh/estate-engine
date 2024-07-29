import logging
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
from django.db import models
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView)

from contracts.models import TenancyContract
from contracts.views import get_filtered_queryset
from properties.forms import TableUnitFilterForm
from properties.models import Document, Property, Unit

from .forms import (CustomPasswordResetForm, CustomSetPasswordForm,
                    ProfilePasswordChangeForm, UserLoginForm, UserProfileForm,
                    UserRegistrationForm)
from .models import User

# Get an instance of a logger
logger = logging.getLogger(__name__)


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('owner_dashboard')

    def form_valid(self, form):
        logger.info('Form is valid in UserRegisterView')
        # super().form_valid(form)
        user = form.save()
        login(self.request, user)
        logger.info(f'User {user.username} registered and logged in')
        if user.role == User.OWNER:
            logger.info('Redirecting to owner dashboard')
            return redirect('owner_dashboard')
        else:
            logger.info('Redirecting to tenant dashboard')
            return redirect('tenant_dashboard')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.OWNER:
            logger.info(f'User {user.email} logged in as owner')
            return reverse_lazy('owner_dashboard')
        else:
            logger.info(f'User {user.email} logged in as tenant')
            return reverse_lazy('tenant_dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.role == User.OWNER:
                return redirect('owner_dashboard')
            else:
                return redirect('tenant_dashboard')
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        logger.info(f'User {request.user.username} logged out')
        return super().dispatch(request, *args, **kwargs)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


class OwnerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/owner_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owner = self.request.user
        context['user'] = owner
        context['total_properties'] = Property.objects.filter(owner=owner).count()
        context['total_units'] = Unit.objects.filter(property__owner=owner).count()
        context['total_tenants'] = TenancyContract.objects.filter(unit__property__owner=owner).count()
        context['tenants_in_contracts'] = TenancyContract.objects.filter(unit__property__owner=owner, active=True).count()
        return context


class TenantDashboardView(TemplateView):
    template_name = 'dashboard/tenant_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tenant = self.request.user

        context['user'] = tenant

        rented_unit_count = Unit.objects.filter(resident=tenant).count()
        context['rented_unit_count'] = rented_unit_count

        total_rent_agreed = TenancyContract.objects.filter(
            tenant=tenant, active=True
        ).aggregate(
            total_rent_agreed=models.Sum('rent_agreed')
        )['total_rent_agreed'] or Decimal('0.00')

        total_rent_agreed = "{:.3f}".format(total_rent_agreed)
        context['total_rent_agreed'] = total_rent_agreed

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'dashboard/profile_update.html'
    success_url = reverse_lazy('profile_update')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Your profile has been updated successfully.')
        return super().form_valid(form)


class PasswordChangeView(LoginRequiredMixin, FormView):
    form_class = ProfilePasswordChangeForm
    template_name = 'dashboard/password_update.html'
    success_url = reverse_lazy('password_change')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, 'Your password has been changed successfully.')
        return super().form_valid(form)


# just to show all approved tenants
class ApprovedTenantsView(ListView):
    template_name = 'users/approved_tenants.html'
    context_object_name = 'approved_documents'
    paginate_by = 20

    def get_queryset(self):
        owner = self.request.user
        queryset = Document.objects.filter(
            status='approved',
            unit__property__owner=owner
        ).select_related(
            'tenant', 'unit', 'unit__property'
        ).prefetch_related(
            Prefetch('tenant', queryset=User.objects.only('id', 'first_name', 'last_name', 'email'))
        )

        self.filter_form = TableUnitFilterForm(self.request.GET, user=owner)
        if self.filter_form.is_valid():
            queryset = get_filtered_queryset(queryset, self.request)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


# to show all tanents
class AllTenantsView(ListView):
    template_name = 'users/all_tenants.html'
    context_object_name = 'all_tenants'
    paginate_by = 20

    def get_queryset(self):
        owner = self.request.user
        queryset = Document.objects.filter(unit__property__owner=owner).select_related(
            'tenant', 'unit', 'unit__property'
        ).prefetch_related(
            Prefetch('tenant', queryset=User.objects.only('id', 'first_name', 'last_name', 'email'))
        )

        self.filter_form = TableUnitFilterForm(self.request.GET, user=owner)
        if self.filter_form.is_valid():
            queryset = get_filtered_queryset(queryset, self.request)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context


# to show profile
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
