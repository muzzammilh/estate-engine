from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic import RedirectView

from .views import LoggingExampleView

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('login'), permanent=True), name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('users.urls')),
    path('property/', include('properties.urls')),
    path('contract/', include('contracts.urls')),
    path('logging/', LoggingExampleView, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
