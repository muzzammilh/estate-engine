from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import CreateView, FormView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm, CustomPasswordResetForm, CustomSetPasswordForm
from .models import User


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('landlord_dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        if user.role == User.LANDLORD:
            return redirect('landlord_dashboard')
        else:
            return redirect('tenant_dashboard')


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        user = self.request.user
        if user.role == User.LANDLORD:
            return reverse_lazy('landlord_dashboard')
        else:
            return reverse_lazy('tenant_dashboard')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')


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

class LandlordDashboardView(TemplateView):
    template_name = 'dashboard/landlord_dashboard.html'


class TenantDashboardView(TemplateView):
    template_name = 'dashboard/tenant_dashboard.html'
