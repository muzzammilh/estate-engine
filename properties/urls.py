from django.urls import path

from .views import (AvailableUnitsView, PropertyCreateView, PropertyDeleteView,
                    PropertyDetailView, PropertyListView, PropertyUpdateView,
                    UnitAppliedTenantsView, UnitCreateView, UnitDeleteView,
                    UnitDetailView, UnitUpdateView, UpdateDocumentStatusView,
                    UploadDocumentsView, UserAppliedUnitsView, load_cities,
                    load_states, load_sub_localities)

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('create/', PropertyCreateView.as_view(), name='property_create'),
    path('<int:pk>/update/', PropertyUpdateView.as_view(), name='property_update'),
    path('<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('<int:property_pk>/unit/create/', UnitCreateView.as_view(), name='unit_create'),
    path('unit/<int:pk>/update/', UnitUpdateView.as_view(), name='unit_update'),
    path('unit/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),
    path('unit/<int:pk>/', UnitDetailView.as_view(), name='unit_detail'),
    path('available-units/', AvailableUnitsView.as_view(), name='available_units'),
    path('user-applied-units/', UserAppliedUnitsView.as_view(), name='user_applied_units'),
    path('unit/<int:unit_id>/applied-tenants/', UnitAppliedTenantsView.as_view(), name='unit_applied_tenants'),
    path('upload-documents/<int:unit_id>', UploadDocumentsView.as_view(), name='upload_documents'),
    path('update-document-status/<int:document_id>/', UpdateDocumentStatusView.as_view(), name='update_document_status'),
    path('ajax/load-states/', load_states, name='ajax_load_states'),
    path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    path('ajax/load-sub-localities/', load_sub_localities, name='ajax_load_sub_localities'),
]
