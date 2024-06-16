from django.urls import path
from django.views.generic import TemplateView

from .views import (CustomPasswordResetCompleteView,
                    CustomPasswordResetConfirmView, CustomPasswordResetView,
                    LandlordDashboardView, PasswordChangeView,
                    ProfileUpdateView, TenantDashboardView, UserLoginView,
                    UserLogoutView, UserRegisterView)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', TemplateView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('landlord-dashboard/', LandlordDashboardView.as_view(), name='landlord_dashboard'),
    path('tenant-dashboard/', TenantDashboardView.as_view(), name='tenant_dashboard'),
    path('profile-update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password-update/', PasswordChangeView.as_view(), name='password_change'),
]
