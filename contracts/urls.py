from django.urls import path

from .views import (ActiveContractsView, AllContractsView, ContractDeleteView,
                    ContractUpdateView, TenancyContractCreateView)

urlpatterns = [
    path('create-contract/<int:tenant_id>/', TenancyContractCreateView.as_view(), name='create_contract'),
    path('active/', ActiveContractsView.as_view(), name='active_contracts'),
    path('all/', AllContractsView.as_view(), name='all_contracts'),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name='update_contract'),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name='delete_contract'),
]
