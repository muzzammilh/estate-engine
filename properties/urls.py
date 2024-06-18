# properties/urls.py

from django.urls import path

from .views import (PropertyCreateView, PropertyDeleteView, PropertyDetailView,
                    PropertyListView, PropertyUpdateView, UnitCreateView,
                    UnitDeleteView, UnitUpdateView, load_cities, load_states,
                    load_sub_localities)

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('property/create/', PropertyCreateView.as_view(), name='property_create'),
    path('property/<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('property/<int:property_pk>/unit/create/', UnitCreateView.as_view(), name='unit_create'),
    path('unit/<int:pk>/update/', UnitUpdateView.as_view(), name='unit_update'),
    path('unit/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
    path('ajax/load-states/', load_states, name='ajax_load_states'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    path('ajax/load-sub-localities/', load_sub_localities, name='ajax_load_sub_localities'),
]
